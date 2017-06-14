import json
import logging
import requests
import traceback

from will import settings

ROOM_NOTIFICATION_URL = "https://%(server)s/v2/room/%(room_id)s/notification?auth_token=%(token)s"
ROOM_TOPIC_URL = "https://%(server)s/v2/room/%(room_id)s/topic?auth_token=%(token)s"
PRIVATE_MESSAGE_URL = "https://%(server)s/v2/user/%(user_id)s/message?auth_token=%(token)s"
SET_TOPIC_URL = "https://%(server)s/v2/room/%(room_id)s/topic?auth_token=%(token)s"
USER_DETAILS_URL = "https://%(server)s/v2/user/%(user_id)s?auth_token=%(token)s"
ALL_USERS_URL = ("https://%(server)s/v2/user?auth_token=%(token)s&start-index"
                 "=%(start_index)s&max-results=%(max_results)s")
ROOM_URL = "https://%(server)s/v2/room"
INVITE_TO_ROOM = "https://%(server)s/v2/room/%(room_id)s/invite/%(user_id)s"

class HipChatMixin(object):

    def send_direct_message(self, user_id, message_body, html=False, notify=False, **kwargs):
        if kwargs:
            logging.warn("Unknown keyword args for send_direct_message: %s" % kwargs)

        format = "text"
        if html:
            format = "html"

        try:
            # https://www.hipchat.com/docs/apiv2/method/private_message_user
            url = PRIVATE_MESSAGE_URL % {"server": settings.HIPCHAT_SERVER,
                                         "user_id": user_id,
                                         "token": settings.V2_TOKEN}
            data = {
                "message": message_body,
                "message_format": format,
                "notify": notify,
            }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, headers=headers, data=json.dumps(data), **settings.REQUESTS_OPTIONS)
        except:
            logging.critical("Error in send_direct_message: \n%s" % traceback.format_exc())

    def send_direct_message_reply(self, message, message_body):
        try:
            message.reply(message_body).send()
        except:
            logging.critical("Error in send_direct_message_reply: \n%s" % traceback.format_exc())

    def send_room_message(self, room_id, message_body, html=False, color="green", notify=False, **kwargs):
        if kwargs:
            logging.warn("Unknown keyword args for send_room_message: %s" % kwargs)

        format = "text"
        if html:
            format = "html"

        try:
            # https://www.hipchat.com/docs/apiv2/method/send_room_notification
            url = ROOM_NOTIFICATION_URL % {"server": settings.HIPCHAT_SERVER,
                                           "room_id": room_id,
                                           "token": settings.V2_TOKEN}
            data = {
                "message": message_body,
                "message_format": format,
                "color": color,
                "notify": notify,
            }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, headers=headers, data=json.dumps(data), **settings.REQUESTS_OPTIONS)
        except:
            logging.critical("Error in send_room_message: \n%s" % traceback.format_exc())

    def set_room_topic(self, room_id, topic):
        try:
            # https://www.hipchat.com/docs/apiv2/method/send_room_notification
            url = ROOM_TOPIC_URL % {"server": settings.HIPCHAT_SERVER,
                                    "room_id": room_id,
                                    "token": settings.V2_TOKEN}
            data = {
                "topic": topic,
            }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.put(url, headers=headers, data=json.dumps(data), **settings.REQUESTS_OPTIONS)
        except:
            logging.critical("Error in set_room_topic: \n%s" % traceback.format_exc())

    def get_hipchat_user(self, user_id, q=None):
        url = USER_DETAILS_URL % {"server": settings.HIPCHAT_SERVER,
                                  "user_id": user_id,
                                  "token": settings.V2_TOKEN}
        r = requests.get(url, **settings.REQUESTS_OPTIONS)
        if q:
            q.put(r.json())
        else:
            return r.json()

    @property
    def full_hipchat_user_list(self):
        if not hasattr(self, "_full_hipchat_user_list"):
            full_roster = {}

            # Grab the first roster page, and populate full_roster
            url = ALL_USERS_URL % {"server": settings.HIPCHAT_SERVER,
                                   "token": settings.V2_TOKEN,
                                   "start_index": 0,
                                   "max_results": 1000}
            r = requests.get(url, **settings.REQUESTS_OPTIONS)
            for user in r.json()['items']:
                full_roster["%s" % (user['id'],)] = user

            # Keep going through the next pages until we're out of pages.
            while 'next' in r.json()['links']:
                url = "%s&auth_token=%s" % (r.json()['links']['next'], settings.V2_TOKEN)
                r = requests.get(url, **settings.REQUESTS_OPTIONS)

                for user in r.json()['items']:
                    full_roster["%s" % (user['id'],)] = user

            self._full_hipchat_user_list = full_roster
        return self._full_hipchat_user_list

    def create_hipchat_room(self, room_name, privacy='public', owner=None,
                            guest_access = False):
        """ create a new hipchat room
            :param room_name: name of the room
            :param privacy: (optional) whether the room is accessible to other users
                            or not
            :param owner_user_id: (optional) the id, email address, or mention
                                name (beginning with an '@') of the room's owner.
                                Defaults to the current user
            :param guest_access: (optional) whether or not guests have access
                                to the room
            :response json:
        """
        url = ROOM_URL % {"server": settings.HIPCHAT_SERVER}
        data = json.dumps({'name': room_name, 'privacy': privacy, 'owner_user_id': owner,
            'guest_access': guest_access})
        params = {'auth_token': settings.V2_TOKEN}
        headers = {'Content-type': 'application/json'}
        try:
            r = requests.post(url, data=data, params=params, headers=headers,
                              **settings.REQUESTS_OPTIONS)
            if r.text:
                logging.debug('Endpoint %(endpoint)s response: \r\n %(resp)s'
                              %{'endpoint': url, 'resp': r.text})
                return r.json()

        except:
            raise

    def invite_user(self, user, room, reason=None):
        """ invite a user to a public room.
            :param user: The id, email address, or mention name of the user
            :param room: The id or url encoded name of the room
            :param reason: (optional) The reason to give to the invited user
        """

        if reason:
            data = json.dumps({'reason': reason})
        else:
            data = None

        url = INVITE_TO_ROOM % {'server': settings.HIPCHAT_SERVER,
                                'room_id': room,
                                'user_id': user}
        params = {'auth_token': settings.V2_TOKEN}
        headers = {'Content-type': 'application/json'}

        try:
            r = requests.post(url, data=data, params=params, headers=headers,
                              **settings.REQUESTS_OPTIONS)

            if r.text:
                logging.debug('Endpoint %(endpoint)s response: \r\n %(resp)s'
                              %{'endpoint': url, 'resp': r.text})
                return r.json()

        except:
            raise

