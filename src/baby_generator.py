from traits import Traits
from person import Person


class BabyGenerator:

    def __init__(self, statistics, names):
        self.statistics = statistics
        self.names = names

    def create_first_child(self, surnames):
        """Generates new child without family to populate city."""
        child = Person(self.statistics.get_gender(), Traits.CHILD.end)
        self.set_first_child_traits(child, surnames)
        self.set_baby_essential_traits(child)
        return child

    def set_first_child_traits(self, child, surnames):
        """Set statistical social class and random surname that is unique among the population."""
        child.surname = self.names.get_surname(surnames)
        child.original_surname = child.surname
        child.race = self.statistics.get_race()
        child.social_class = self.statistics.get_social_class()

    def set_baby_essential_traits(self, baby):
        """Gives baby a random name, target gender, death date/cause and fertility."""
        baby.name = self.names.get_name(baby)
        baby.death_date = self.statistics.get_death_date()
        baby.death_cause = self.statistics.get_death_cause(baby)
        baby.can_have_bio_children = self.statistics.get_fertility()

    def generate_baby(self, couple):
        """Generates baby from given couple."""
        baby = Person(self.statistics.get_gender(), Traits.BABY.start)
        self.link_family(baby, couple)
        self.set_baby_essential_traits(baby)
        self.baby_validation(baby)
        return baby

    @classmethod
    def link_family(cls, baby, couple):
        """Assign's baby's family."""
        baby.parents.extend(couple.persons)
        for parent in baby.parents:
            parent.children.append(baby)
        baby.social_class = baby.parents[0].social_class
        baby.race = baby.parents[0].race  # This must be changed

        if couple.is_straight:
            baby.surname = couple.man.surname
            baby.apartment_id = couple.woman.apartment_id
        else:
            baby.surname = baby.parents[0].surname
            baby.apartment_id = baby.parents[0].apartment_id
        baby.original_surname = baby.surname

    @classmethod
    def baby_validation(cls, baby):
        """Validates baby's correct traits and family."""
        # Baby attributes
        if baby.name is None:
            raise Exception("Person has no name.")
        if baby.surname is None or baby.original_surname is None:
            raise Exception("Person has no surname.")
        if baby.stage is None or baby.stage not in Traits.LIFESTAGES:
            raise Exception("Person's life stage is wrong.")
        if baby.age is None or baby.age not in baby.stage.span or baby.age not in Traits.LIFESPAN:
            raise Exception("Person's age is wrong.")
        if baby.gender is None or baby.gender not in Traits.GENDERS:
            raise Exception("Person's gender is wrong.")
        if baby.death_cause is None or baby.death_cause not in Traits.DEATH_CAUSES:
            raise Exception("Person's death cause is wrong.")
        if baby.death_date is not False and baby.death_date not in Traits.LIFESPAN:
            raise Exception("Person's death date is wrong.")

        # Family
        if len(baby.bio_family) == 0:
            raise Exception("Baby's family is null.")
        if baby in baby.bio_family:
            raise Exception("Baby is inside his relatives list.")
        if len(baby.parents) <= 0 and len(baby.adoptive_parents) <= 0:
            raise Exception("Baby has no parents.")
        if len(set(baby.parents)) != len(baby.parents):
            raise Exception("List of parents contains duplicates.")
        for parent in baby.parents:
            if len(set(parent.children)) != len(parent.children):
                raise Exception("List of children contains duplicates.")
        # Siblings
        if len(set(baby.full_siblings)) != len(baby.full_siblings):
            raise Exception("List of siblings contains duplicates.")
        for sibling in baby.full_siblings:
            if sibling in [baby.half_siblings, baby.step_siblings, baby.adoptive_full_siblings]:
                raise Exception("Full-sibling inside list of half/step/adoptive siblings.")
        for half_sib in baby.half_siblings:
            if half_sib in [baby.full_siblings, baby.step_siblings, baby.adoptive_full_siblings]:
                raise Exception("Half-sibling inside list of full/step/adoptive siblings.")
        for step_sib in baby.half_siblings:
            if step_sib in [baby.full_siblings, baby.half_siblings, baby.adoptive_full_siblings]:
                raise Exception("Step-sibling inside list of full/half/adoptive siblings.")
        for adoptive_sib in baby.half_siblings:
            if adoptive_sib in [baby.full_siblings, baby.half_siblings, baby.step_siblings]:
                raise Exception("Adoptive sibling inside list of full/half/step siblings.")
        # Twin and triplets
        if baby.is_twin:
            if len(baby.siblings) == 0:
                raise Exception("Baby is twin but has no siblings.")
            if all([baby.is_twin is False for sibling in baby.siblings]):
                raise Exception("Baby is twin but has no twin sibling.")
        if baby.is_triplet:
            if len(baby.siblings) < 2:
                raise Exception(
                    "Baby is triplet but has an incorrect number of siblings.")
            if sum(1 for sibling in baby.siblings if sibling.is_triplet) < 2:
                raise Exception(
                    "Baby is triplet but has no triplet siblings.")
