from Snapshottable import Snapshottable

class Human(Snapshottable):
    def __init__(self, transaction_date, interests=None, vocabulary=None, knowledge=None, memories=None, accomplishments=None, relationships=None, family=None, home=None, diet=None, sleep_schedule=None, medical_history=None, political_opinions=None, career=None, aspirations=None, romance=None, entertainment=None, skills=None, pleasures=None, reading_level_scores=None, communication_styles=None, emotions=None, best_communication_method=None):
        super().__init__(Human, transaction_date)

        self.conversations = []
        self.memories = []

        self.reading_level_scores = reading_level_scores or []
        self.communication_styles = communication_styles or []
        self.emotions = emotions or []
        self.best_communication_method = best_communication_method

        self.interests = interests or []
        self.vocabulary = vocabulary or []
        self.knowledge = knowledge or []
        self.memories = memories or []
        self.accomplishments = accomplishments or []
        self.relationships = relationships or []
        self.family = family or []
        self.home = home
        self.diet = diet or []
        self.sleep_schedule = sleep_schedule
        self.medical_history = medical_history or []
        self.political_opinions = political_opinions or []
        self.career = career
        self.aspirations = aspirations or []
        self.romance = romance
        self.entertainment = entertainment or []
        self.skills = skills or []
        self.pleasures = pleasures or []


def clone_without_snapshots(self):
    # Create a dictionary copy of the current object's __dict__
    clone_dict = self.__dict__.copy()

    # Remove the snapshots array from the cloned dictionary
    clone_dict.pop('snapshots', None)

    # Create a new instance of the Human class
    cloned_obj = Human(transaction_date=None)

    # Update the __dict__ of the new object with the cloned dictionary
    cloned_obj.__dict__.update(clone_dict)

    return cloned_obj