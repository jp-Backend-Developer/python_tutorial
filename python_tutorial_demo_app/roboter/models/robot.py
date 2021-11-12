from roboter.views import console
from roboter.models import ranking

DEFAULT_ROBOT_NAME = 'Pepper'


class Robot(object):
    """base model for Robot."""

    def __init__(self, name=DEFAULT_ROBOT_NAME, user_name='',
                 speak_color='green'):
        self.name = name
        self.user_name = user_name
        self.speak_color = speak_color

    def hello(self):
        """Return words tp user that the robot speaks at the beginning"""
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            user_name = input(template.substitute({
                'robot_name': self.name
            }))

            if user_name:
                self.user_name = user_name.title()
                break


class RestaurantRobot(Robot):
    """Handle data model on dinner"""
    def __init__(self, name=DEFAULT_ROBOT_NAME):
        super().__init__(name=name)
        self.ranking_model = ranking.RankingModel()

    def recommend_restaurant(self):
        """Show restaurant recommended restaurant to the user."""
        new_recommend_restaurant = self.ranking_model.get_most_popular()
        if not new_recommend_restaurant:
            return None

        will_recommend_restaurant = [new_recommend_restaurant]
        while True:
            template = console.get_template('greeting.txt', self.speak_color)
            is_yes = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'restaurant': new_recommend_restaurant
            }))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_restaurant = self.ranking_model.get_most_popular(
                    not_list=will_recommend_restaurant
                )
                if not new_recommend_restaurant:
                    break
                will_recommend_restaurant.append(new_recommend_restaurant)

    def ask_user_favorite(self):
        """Collect favorite restaurant information from users."""
        while True:
            template = console.get_template(
                'which_restaurant.txt', self.speak_color
            )
            restaurant = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))
            if restaurant:
                self.ranking_model.increment(restaurant)
                break

    def thank_you(self):
        """Show words of appreciation to users."""
        template = console.get_template('good_by.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name
        }))
