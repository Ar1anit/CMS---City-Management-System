import json

class JSONFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def set_sid(self, user, sid):
        self.data.setdefault(user, {})
        self.data[user]["chat_id"] = sid
        self.save_data()
        return self.data[user]["chat_id"] == sid

    def get_sid(self, user):
        return self.data.get(user, {}).get("chat_id")

    def set_current_chat(self, user, chat_partner):
        self.data[user]["current_chat"] = chat_partner
        self.save_data()
        return self.data[user]["current_chat"] == chat_partner

    def get_current_chat(self, user):
        return self.data[user]["current_chat"]

    def create_user(self, username):
        self.data.setdefault(username, {"chat_id": "None", "current_chat": "None"})
        self.save_data()

    #
    # GROUP CHAT RELATED
    #

    def create_group_chat(self, group_chat_name):
        self.data.setdefault(group_chat_name, {"members": []})
        self.save_data()

    def get_group_chats(self):
        return self.data.keys()

    def add_group_chat_member(self, group_chat, member):
        self.data[group_chat]["members"].append(member)
        self.save_data()

    def get_group_chat_members(self, group_name):
        return self.data[group_name]["members"]

    def user_is_in_group(self, group_name, user):

        return user in self.get_group_chat_members(group_name)


    #
    # PROFILE VISIBILITY
    #

    def set_profile_visibility(self, user, visibility):

        self.data[user] = visibility
        self.save_data()

    def get_profile_visibility(self, user):

        return self.data[user]

    #
    # PROFILE DIAGRAMS
    #

    def add_diagram(self, user, url, name):

        if not self.data:
            self.data = [{user: []}]

        if user not in self.data[0]:
            self.data[0][user] = []

        self.data[0][user].append(
                            {
                                'url': url,
                                'name': name.replace("_", " ")
                            }
                          )

        self.save_data()

    def get_diagrams(self, user):
        """
        Retrieve added diagrams, may also be used to load data
        :param user: The user you want to get the diagrams of
        :return: the diagrams
        """

        if not self.data:
            self.data = [{user: []}]

        if user not in self.data[0]:
            self.data[0][user] = []

        return self.data[0][user]

    def clear_added_diagrams(self, user):

        self.data[0][user] = []


if __name__ == "__main__":
    x = JSONFileManager("../datasets/user_added_diagrams.json")
