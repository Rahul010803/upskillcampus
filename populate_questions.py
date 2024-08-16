import os
import django
from django.core.management.base import BaseCommand
from app.models import Question, Level, Subject  # Adjust import paths as needed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

class Command(BaseCommand):
    help = 'Populate the Question model with predefined questions'

    def handle(self, *args, **kwargs):
        # Define Levels
        levels = {
            1: 'Level 1',
            2: 'Level 2',
            3: 'Level 3',
            4: 'Level 4',
            5: 'Level 5'
        }
        for level in levels.values():
            Level.objects.get_or_create(name=level)
        
        # Define Subjects
        subjects = ['Physics', 'Mathematics', 'Music', 'History', 'Geography', 'Literature', 'Science', 'Art', 'Sports',]
        for subject in subjects:
            Subject.objects.get_or_create(name=subject)
            
            
        questions = [
            #Physics
            # Level 1
            {
                'question_text': 'What is the SI unit of force?',
                'option_1': 'Newton',
                'option_2': 'Joule',
                'option_3': 'Watt',
                'option_4': 'Pascal',
                'correct_answer': 'Newton',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the speed of light in vacuum?',
                'option_1': '3 x 10^8 m/s',
                'option_2': '3 x 10^6 m/s',
                'option_3': '3 x 10^5 m/s',
                'option_4': '3 x 10^7 m/s',
                'correct_answer': '3 x 10^8 m/s',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which planet is known as the Red Planet?',
                'option_1': 'Earth',
                'option_2': 'Mars',
                'option_3': 'Jupiter',
                'option_4': 'Venus',
                'correct_answer': 'Mars',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the acceleration due to gravity on Earth?',
                'option_1': '9.8 m/s^2',
                'option_2': '9.6 m/s^2',
                'option_3': '10 m/s^2',
                'option_4': '9.2 m/s^2',
                'correct_answer': '9.8 m/s^2',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a scalar quantity?',
                'option_1': 'Velocity',
                'option_2': 'Acceleration',
                'option_3': 'Force',
                'option_4': 'Energy',
                'correct_answer': 'Energy',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the boiling point of water in Celsius?',
                'option_1': '90°C',
                'option_2': '80°C',
                'option_3': '100°C',
                'option_4': '110°C',
                'correct_answer': '100°C',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a vector quantity?',
                'option_1': 'Speed',
                'option_2': 'Work',
                'option_3': 'Power',
                'option_4': 'Displacement',
                'correct_answer': 'Displacement',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a non-renewable resource?',
                'option_1': 'Solar energy',
                'option_2': 'Wind energy',
                'option_3': 'Coal',
                'option_4': 'Geothermal energy',
                'correct_answer': 'Coal',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the chemical symbol for water?',
                'option_1': 'O2',
                'option_2': 'H2O',
                'option_3': 'CO2',
                'option_4': 'N2',
                'correct_answer': 'H2O',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the main gas found in the air we breathe?',
                'option_1': 'Oxygen',
                'option_2': 'Nitrogen',
                'option_3': 'Carbon Dioxide',
                'option_4': 'Hydrogen',
                'correct_answer': 'Nitrogen',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is an example of potential energy?',
                'option_1': 'A moving car',
                'option_2': 'A stretched spring',
                'option_3': 'Flowing water',
                'option_4': 'A falling apple',
                'correct_answer': 'A stretched spring',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the atomic number of hydrogen?',
                'option_1': '1',
                'option_2': '2',
                'option_3': '3',
                'option_4': '4',
                'correct_answer': '1',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the unit of electric current?',
                'option_1': 'Volt',
                'option_2': 'Ampere',
                'option_3': 'Ohm',
                'option_4': 'Watt',
                'correct_answer': 'Ampere',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the formula for calculating speed?',
                'option_1': 'Speed = Distance × Time',
                'option_2': 'Speed = Distance / Time',
                'option_3': 'Speed = Time / Distance',
                'option_4': 'Speed = Distance + Time',
                'correct_answer': 'Speed = Distance / Time',
                'level': 1,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the common name for sodium chloride?',
                'option_1': 'Sugar',
                'option_2': 'Salt',
                'option_3': 'Baking soda',
                'option_4': 'Vinegar',
                'correct_answer': 'Salt',
                'level': 1,
                'subject': 'Physics'
            },
            # Level 2
            {
                'question_text': 'What is the primary function of a battery in an electrical circuit?',
                'option_1': 'To increase resistance',
                'option_2': 'To provide current',
                'option_3': 'To store energy',
                'option_4': 'To increase voltage',
                'correct_answer': 'To store energy',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which law states that the current through a conductor between two points is directly proportional to the voltage across the two points?',
                'option_1': 'Newton’s First Law',
                'option_2': 'Ohm’s Law',
                'option_3': 'Faraday’s Law',
                'option_4': 'Coulomb’s Law',
                'correct_answer': 'Ohm’s Law',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the acceleration of an object in free fall under gravity (ignoring air resistance)?',
                'option_1': '9.8 m/s',
                'option_2': '9.8 m/s^2',
                'option_3': '10 m/s',
                'option_4': '10 m/s^2',
                'correct_answer': '9.8 m/s^2',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'What type of mirror is used to focus light to a point?',
                'option_1': 'Plane mirror',
                'option_2': 'Convex mirror',
                'option_3': 'Concave mirror',
                'option_4': 'Spherical mirror',
                'correct_answer': 'Concave mirror',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is not a type of electromagnetic radiation?',
                'option_1': 'Radio waves',
                'option_2': 'Sound waves',
                'option_3': 'X-rays',
                'option_4': 'Gamma rays',
                'correct_answer': 'Sound waves',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which physical quantity is measured in joules?',
                'option_1': 'Force',
                'option_2': 'Work',
                'option_3': 'Power',
                'option_4': 'Velocity',
                'correct_answer': 'Work',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the name of the force that opposes motion between two surfaces?',
                'option_1': 'Gravity',
                'option_2': 'Magnetic force',
                'option_3': 'Friction',
                'option_4': 'Electrostatic force',
                'correct_answer': 'Friction',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which gas is most abundant in Earth’s atmosphere?',
                'option_1': 'Oxygen',
                'option_2': 'Nitrogen',
                'option_3': 'Carbon Dioxide',
                'option_4': 'Helium',
                'correct_answer': 'Nitrogen',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the power dissipated by a resistor if the current through it is 2 A and the resistance is 4 ohms?',
                'option_1': '8 W',
                'option_2': '16 W',
                'option_3': '32 W',
                'option_4': '4 W',
                'correct_answer': '16 W',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following elements is a non-metal?',
                'option_1': 'Iron',
                'option_2': 'Gold',
                'option_3': 'Oxygen',
                'option_4': 'Silver',
                'correct_answer': 'Oxygen',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following phenomena explains the blue color of the sky?',
                'option_1': 'Reflection',
                'option_2': 'Refraction',
                'option_3': 'Scattering',
                'option_4': 'Diffraction',
                'correct_answer': 'Scattering',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the speed of sound in air?',
                'option_1': '300 m/s',
                'option_2': '330 m/s',
                'option_3': '340 m/s',
                'option_4': '360 m/s',
                'correct_answer': '340 m/s',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which principle states that the buoyant force on an object is equal to the weight of the fluid displaced by the object?',
                'option_1': 'Pascal’s Principle',
                'option_2': 'Archimedes’ Principle',
                'option_3': 'Bernoulli’s Principle',
                'option_4': 'Boyle’s Law',
                'correct_answer': 'Archimedes’ Principle',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a renewable energy resource?',
                'option_1': 'Natural Gas',
                'option_2': 'Oil',
                'option_3': 'Coal',
                'option_4': 'Solar Energy',
                'correct_answer': 'Solar Energy',
                'level': 2,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a derived quantity in the International System of Units (SI)?',
                'option_1': 'Mass',
                'option_2': 'Length',
                'option_3': 'Time',
                'option_4': 'Velocity',
                'correct_answer': 'Velocity',
                'level': 2,
                'subject': 'Physics'
            },
            # Level 3
            {
                'question_text': 'What is the escape velocity from Earth’s surface?',
                'option_1': '8 km/s',
                'option_2': '11.2 km/s',
                'option_3': '15 km/s',
                'option_4': '7.8 km/s',
                'correct_answer': '11.2 km/s',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following particles is a fermion?',
                'option_1': 'Photon',
                'option_2': 'Neutrino',
                'option_3': 'Gluon',
                'option_4': 'Graviton',
                'correct_answer': 'Neutrino',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the value of Planck’s constant?',
                'option_1': '6.63 x 10^-34 J·s',
                'option_2': '3.00 x 10^8 J·s',
                'option_3': '1.60 x 10^-19 J·s',
                'option_4': '9.81 x 10^-31 J·s',
                'correct_answer': '6.63 x 10^-34 J·s',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a unit of inductance?',
                'option_1': 'Farad',
                'option_2': 'Henry',
                'option_3': 'Coulomb',
                'option_4': 'Weber',
                'correct_answer': 'Henry',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the primary function of a transformer?',
                'option_1': 'To store energy',
                'option_2': 'To convert AC to DC',
                'option_3': 'To increase or decrease voltage',
                'option_4': 'To convert electrical energy into mechanical energy',
                'correct_answer': 'To increase or decrease voltage',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the threshold frequency in the context of the photoelectric effect?',
                'option_1': 'The frequency below which no electrons are emitted',
                'option_2': 'The frequency at which maximum electrons are emitted',
                'option_3': 'The frequency above which electrons stop being emitted',
                'option_4': 'The frequency at which light is absorbed completely',
                'correct_answer': 'The frequency below which no electrons are emitted',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which law describes the force between two charged objects?',
                'option_1': 'Newton’s Second Law',
                'option_2': 'Coulomb’s Law',
                'option_3': 'Ohm’s Law',
                'option_4': 'Faraday’s Law',
                'correct_answer': 'Coulomb’s Law',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the unit of the magnetic field?',
                'option_1': 'Tesla',
                'option_2': 'Henry',
                'option_3': 'Volt',
                'option_4': 'Ohm',
                'correct_answer': 'Tesla',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is an application of superconductors?',
                'option_1': 'Semiconductors',
                'option_2': 'Maglev trains',
                'option_3': 'Electric heaters',
                'option_4': 'Incandescent bulbs',
                'correct_answer': 'Maglev trains',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the principle of operation of a nuclear reactor?',
                'option_1': 'Fusion',
                'option_2': 'Fission',
                'option_3': 'Radiation',
                'option_4': 'Convection',
                'correct_answer': 'Fission',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a correct statement about wave-particle duality?',
                'option_1': 'Particles exhibit wave-like properties only in motion',
                'option_2': 'Waves can behave like particles',
                'option_3': 'Particles can never exhibit wave-like properties',
                'option_4': 'Wave-particle duality is an outdated concept',
                'correct_answer': 'Waves can behave like particles',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following elements has the highest electrical conductivity?',
                'option_1': 'Copper',
                'option_2': 'Silver',
                'option_3': 'Gold',
                'option_4': 'Aluminum',
                'correct_answer': 'Silver',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is the best description of an ideal gas?',
                'option_1': 'A gas that does not condense',
                'option_2': 'A gas with no interactions between molecules',
                'option_3': 'A gas that follows Boyle’s law at all temperatures',
                'option_4': 'A gas with variable specific heat',
                'correct_answer': 'A gas with no interactions between molecules',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the color of light emitted by a sodium vapor lamp?',
                'option_1': 'Blue',
                'option_2': 'Red',
                'option_3': 'Yellow',
                'option_4': 'Green',
                'correct_answer': 'Yellow',
                'level': 3,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which phenomenon demonstrates the wave nature of light?',
                'option_1': 'Photoelectric effect',
                'option_2': 'Blackbody radiation',
                'option_3': 'Diffraction',
                'option_4': 'Pair production',
                'correct_answer': 'Diffraction',
                'level': 3,
                'subject': 'Physics'
            },
             {
                'question_text': 'What is the main source of energy in the Sun?',
                'option_1': 'Nuclear Fission',
                'option_2': 'Nuclear Fusion',
                'option_3': 'Chemical Reactions',
                'option_4': 'Gravitational Contraction',
                'correct_answer': 'Nuclear Fusion',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following particles has no electrical charge?',
                'option_1': 'Proton',
                'option_2': 'Electron',
                'option_3': 'Neutron',
                'option_4': 'Positron',
                'correct_answer': 'Neutron',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which law explains why a boat floats on water?',
                'option_1': 'Pascal’s Law',
                'option_2': 'Archimedes’ Principle',
                'option_3': 'Boyle’s Law',
                'option_4': 'Bernoulli’s Principle',
                'correct_answer': 'Archimedes’ Principle',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is the correct unit of energy?',
                'option_1': 'Newton',
                'option_2': 'Joule',
                'option_3': 'Watt',
                'option_4': 'Volt',
                'correct_answer': 'Joule',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the velocity of an object in free fall near the Earth’s surface after 3 seconds, neglecting air resistance?',
                'option_1': '9.8 m/s',
                'option_2': '19.6 m/s',
                'option_3': '29.4 m/s',
                'option_4': '39.2 m/s',
                'correct_answer': '29.4 m/s',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the phenomenon of splitting light into its component colors called?',
                'option_1': 'Reflection',
                'option_2': 'Refraction',
                'option_3': 'Diffraction',
                'option_4': 'Dispersion',
                'correct_answer': 'Dispersion',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following elements has the highest melting point?',
                'option_1': 'Iron',
                'option_2': 'Tungsten',
                'option_3': 'Gold',
                'option_4': 'Copper',
                'correct_answer': 'Tungsten',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the term for the bending of waves around obstacles?',
                'option_1': 'Diffraction',
                'option_2': 'Refraction',
                'option_3': 'Reflection',
                'option_4': 'Interference',
                'correct_answer': 'Diffraction',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which type of wave requires a medium to travel through?',
                'option_1': 'Electromagnetic waves',
                'option_2': 'Mechanical waves',
                'option_3': 'Gravitational waves',
                'option_4': 'Matter waves',
                'correct_answer': 'Mechanical waves',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following is a vector quantity?',
                'option_1': 'Speed',
                'option_2': 'Time',
                'option_3': 'Temperature',
                'option_4': 'Velocity',
                'correct_answer': 'Velocity',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the primary cause of tides on Earth?',
                'option_1': 'Solar radiation',
                'option_2': 'Wind currents',
                'option_3': 'Gravitational pull of the Moon',
                'option_4': 'Earth’s rotation',
                'correct_answer': 'Gravitational pull of the Moon',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the SI unit of electric charge?',
                'option_1': 'Coulomb',
                'option_2': 'Ampere',
                'option_3': 'Volt',
                'option_4': 'Farad',
                'correct_answer': 'Coulomb',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What does the term "absolute zero" refer to?',
                'option_1': '0°C',
                'option_2': '273°C',
                'option_3': '0 K',
                'option_4': '273 K',
                'correct_answer': '0 K',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following principles is used in rocket propulsion?',
                'option_1': 'Archimedes’ Principle',
                'option_2': 'Pascal’s Law',
                'option_3': 'Newton’s Third Law of Motion',
                'option_4': 'Bernoulli’s Principle',
                'correct_answer': 'Newton’s Third Law of Motion',
                'level': 4,
                'subject': 'Physics'
            },
            {
                'question_text': 'What does the term "latent heat" refer to?',
                'option_1': 'Heat energy required to change the state of a substance',
                'option_2': 'Heat energy that increases the temperature of a substance',
                'option_3': 'Heat energy lost during a reaction',
                'option_4': 'Heat energy stored in a system',
                'correct_answer': 'Heat energy required to change the state of a substance',
                'level': 4,
                'subject': 'Physics'
            },
            # Level 5
            {
                'question_text': 'What is the principle of equivalence in general relativity?',
                'option_1': 'The idea that the gravitational force is equivalent to a fictitious force',
                'option_2': 'The idea that gravitational mass and inertial mass are equivalent',
                'option_3': 'The principle that light has a constant speed in all reference frames',
                'option_4': 'The principle that energy and mass are equivalent',
                'correct_answer': 'The idea that gravitational mass and inertial mass are equivalent',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which fundamental force is responsible for holding the nucleus of an atom together?',
                'option_1': 'Gravitational Force',
                'option_2': 'Electromagnetic Force',
                'option_3': 'Strong Nuclear Force',
                'option_4': 'Weak Nuclear Force',
                'correct_answer': 'Strong Nuclear Force',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'In quantum mechanics, what is the Heisenberg Uncertainty Principle?',
                'option_1': 'The principle that energy is quantized',
                'option_2': 'The principle that particles have both wave and particle properties',
                'option_3': 'The principle that it is impossible to simultaneously know the exact position and momentum of a particle',
                'option_4': 'The principle that electrons orbit the nucleus in fixed paths',
                'correct_answer': 'The principle that it is impossible to simultaneously know the exact position and momentum of a particle',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What phenomenon is described by Einstein’s theory of special relativity?',
                'option_1': 'Gravitational Waves',
                'option_2': 'Time Dilation',
                'option_3': 'Black Hole Formation',
                'option_4': 'Wave-Particle Duality',
                'correct_answer': 'Time Dilation',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the significance of the Higgs boson in particle physics?',
                'option_1': 'It explains the origin of the electromagnetic force',
                'option_2': 'It is responsible for giving particles mass',
                'option_3': 'It explains the behavior of dark matter',
                'option_4': 'It is a force-carrying particle',
                'correct_answer': 'It is responsible for giving particles mass',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which equation represents the conservation of energy in a relativistic system?',
                'option_1': 'E = mc^2',
                'option_2': 'E = hv',
                'option_3': 'F = ma',
                'option_4': 'V = IR',
                'correct_answer': 'E = mc^2',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which type of particle is associated with the weak nuclear force?',
                'option_1': 'Photon',
                'option_2': 'Gluon',
                'option_3': 'W and Z bosons',
                'option_4': 'Higgs boson',
                'correct_answer': 'W and Z bosons',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the relationship between frequency and wavelength for a wave?',
                'option_1': 'Directly proportional',
                'option_2': 'Inversely proportional',
                'option_3': 'Unrelated',
                'option_4': 'Proportional to the square of amplitude',
                'correct_answer': 'Inversely proportional',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the purpose of a wave function in quantum mechanics?',
                'option_1': 'To describe the particle’s energy level',
                'option_2': 'To predict the exact position of a particle',
                'option_3': 'To describe the probability distribution of a particle’s position',
                'option_4': 'To determine the particle’s velocity',
                'correct_answer': 'To describe the probability distribution of a particle’s position',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following describes a superconducting material?',
                'option_1': 'A material that has infinite resistance',
                'option_2': 'A material that conducts electricity without resistance at low temperatures',
                'option_3': 'A material that emits radiation when cooled',
                'option_4': 'A material that does not conduct electricity',
                'correct_answer': 'A material that conducts electricity without resistance at low temperatures',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the main difference between a fermion and a boson?',
                'option_1': 'Fermions obey the Pauli exclusion principle; bosons do not',
                'option_2': 'Bosons have mass; fermions do not',
                'option_3': 'Fermions can occupy the same quantum state; bosons cannot',
                'option_4': 'Bosons are force carriers; fermions are not',
                'correct_answer': 'Fermions obey the Pauli exclusion principle; bosons do not',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the term for the resistance of an object to changes in its state of motion?',
                'option_1': 'Inertia',
                'option_2': 'Momentum',
                'option_3': 'Force',
                'option_4': 'Energy',
                'correct_answer': 'Inertia',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the cosmological constant, as introduced by Einstein?',
                'option_1': 'A constant used to describe the rate of expansion of the universe',
                'option_2': 'A constant that determines the strength of the gravitational force',
                'option_3': 'A term used to prevent a dynamic universe model',
                'option_4': 'A constant related to the speed of light',
                'correct_answer': 'A term used to prevent a dynamic universe model',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'What is the primary cause of magnetic fields?',
                'option_1': 'Gravitational forces',
                'option_2': 'Motion of charged particles',
                'option_3': 'Thermal energy',
                'option_4': 'Nuclear forces',
                'correct_answer': 'Motion of charged particles',
                'level': 5,
                'subject': 'Physics'
            },
            {
                'question_text': 'Which of the following best describes a black hole?',
                'option_1': 'A massive star that has collapsed into a singularity',
                'option_2': 'A region of space where the escape velocity exceeds the speed of light',
                'option_3': 'A void in space where no matter exists',
                'option_4': 'A dense neutron star',
                'correct_answer': 'A region of space where the escape velocity exceeds the speed of light',
                'level': 5,
                'subject': 'Physics'
            },   
            # Mathematics
            # Level 1
            {
                'question_text': 'What is 5 + 3?',
                'option_1': '7',
                'option_2': '8',
                'option_3': '9',
                'option_4': '10',
                'correct_answer': '8',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 7 - 4?',
                'option_1': '3',
                'option_2': '4',
                'option_3': '5',
                'option_4': '6',
                'correct_answer': '3',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 9 * 2?',
                'option_1': '16',
                'option_2': '18',
                'option_3': '20',
                'option_4': '22',
                'correct_answer': '18',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 10 ÷ 2?',
                'option_1': '3',
                'option_2': '4',
                'option_3': '5',
                'option_4': '6',
                'correct_answer': '5',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the next number in the sequence: 2, 4, 6, ?',
                'option_1': '7',
                'option_2': '8',
                'option_3': '9',
                'option_4': '10',
                'correct_answer': '8',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'Which number is the smallest?',
                'option_1': '3',
                'option_2': '5',
                'option_3': '2',
                'option_4': '4',
                'correct_answer': '2',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 15 - 9?',
                'option_1': '5',
                'option_2': '6',
                'option_3': '7',
                'option_4': '8',
                'correct_answer': '6',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 6 + 7?',
                'option_1': '12',
                'option_2': '13',
                'option_3': '14',
                'option_4': '15',
                'correct_answer': '13',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 3 * 4?',
                'option_1': '10',
                'option_2': '11',
                'option_3': '12',
                'option_4': '13',
                'correct_answer': '12',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square of 3?',
                'option_1': '6',
                'option_2': '8',
                'option_3': '9',
                'option_4': '12',
                'correct_answer': '9',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 10 + 5?',
                'option_1': '14',
                'option_2': '15',
                'option_3': '16',
                'option_4': '17',
                'correct_answer': '15',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 12 - 8?',
                'option_1': '2',
                'option_2': '3',
                'option_3': '4',
                'option_4': '5',
                'correct_answer': '4',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 2 * 7?',
                'option_1': '12',
                'option_2': '13',
                'option_3': '14',
                'option_4': '15',
                'correct_answer': '14',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 18 ÷ 3?',
                'option_1': '4',
                'option_2': '5',
                'option_3': '6',
                'option_4': '7',
                'correct_answer': '6',
                'level': 1,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'Which number is the largest?',
                'option_1': '12',
                'option_2': '15',
                'option_3': '14',
                'option_4': '13',
                'correct_answer': '15',
                'level': 1,
                'subject': 'Mathematics'
            },
            # Level 2
            {
                'question_text': 'What is 12 * 2?',
                'option_1': '22',
                'option_2': '24',
                'option_3': '26',
                'option_4': '28',
                'correct_answer': '24',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 36 ÷ 6?',
                'option_1': '5',
                'option_2': '6',
                'option_3': '7',
                'option_4': '8',
                'correct_answer': '6',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 25 + 15?',
                'option_1': '40',
                'option_2': '41',
                'option_3': '42',
                'option_4': '43',
                'correct_answer': '40',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 7 * 3?',
                'option_1': '20',
                'option_2': '21',
                'option_3': '22',
                'option_4': '23',
                'correct_answer': '21',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square root of 16?',
                'option_1': '2',
                'option_2': '3',
                'option_3': '4',
                'option_4': '5',
                'correct_answer': '4',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 15 * 3?',
                'option_1': '45',
                'option_2': '46',
                'option_3': '47',
                'option_4': '48',
                'correct_answer': '45',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 64 ÷ 8?',
                'option_1': '6',
                'option_2': '7',
                'option_3': '8',
                'option_4': '9',
                'correct_answer': '8',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 9 squared?',
                'option_1': '18',
                'option_2': '27',
                'option_3': '36',
                'option_4': '81',
                'correct_answer': '81',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of 23 and 34?',
                'option_1': '56',
                'option_2': '57',
                'option_3': '58',
                'option_4': '59',
                'correct_answer': '57',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 48 ÷ 6?',
                'option_1': '6',
                'option_2': '7',
                'option_3': '8',
                'option_4': '9',
                'correct_answer': '8',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 18 * 2?',
                'option_1': '32',
                'option_2': '34',
                'option_3': '36',
                'option_4': '38',
                'correct_answer': '36',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 7 + 8?',
                'option_1': '14',
                'option_2': '15',
                'option_3': '16',
                'option_4': '17',
                'correct_answer': '15',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square of 8?',
                'option_1': '48',
                'option_2': '56',
                'option_3': '64',
                'option_4': '72',
                'correct_answer': '64',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 9 * 4?',
                'option_1': '32',
                'option_2': '34',
                'option_3': '36',
                'option_4': '38',
                'correct_answer': '36',
                'level': 2,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the cube root of 27?',
                'option_1': '2',
                'option_2': '3',
                'option_3': '4',
                'option_4': '5',
                'correct_answer': '3',
                'level': 2,
                'subject': 'Mathematics'
            },
            # Level 3
            {
                'question_text': 'What is 12 * 12?',
                'option_1': '132',
                'option_2': '142',
                'option_3': '144',
                'option_4': '146',
                'correct_answer': '144',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 81 ÷ 9?',
                'option_1': '7',
                'option_2': '8',
                'option_3': '9',
                'option_4': '10',
                'correct_answer': '9',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square root of 121?',
                'option_1': '10',
                'option_2': '11',
                'option_3': '12',
                'option_4': '13',
                'correct_answer': '11',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 15 * 8?',
                'option_1': '110',
                'option_2': '120',
                'option_3': '130',
                'option_4': '140',
                'correct_answer': '120',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the cube of 3?',
                'option_1': '9',
                'option_2': '18',
                'option_3': '27',
                'option_4': '36',
                'correct_answer': '27',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the product of 14 and 6?',
                'option_1': '64',
                'option_2': '74',
                'option_3': '84',
                'option_4': '94',
                'correct_answer': '84',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of 123 and 234?',
                'option_1': '345',
                'option_2': '357',
                'option_3': '367',
                'option_4': '377',
                'correct_answer': '357',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square root of 225?',
                'option_1': '13',
                'option_2': '14',
                'option_3': '15',
                'option_4': '16',
                'correct_answer': '15',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 50 * 2?',
                'option_1': '90',
                'option_2': '100',
                'option_3': '110',
                'option_4': '120',
                'correct_answer': '100',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 24 squared?',
                'option_1': '484',
                'option_2': '576',
                'option_3': '676',
                'option_4': '776',
                'correct_answer': '576',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 13 * 13?',
                'option_1': '149',
                'option_2': '159',
                'option_3': '169',
                'option_4': '179',
                'correct_answer': '169',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 1000 ÷ 10?',
                'option_1': '90',
                'option_2': '100',
                'option_3': '110',
                'option_4': '120',
                'correct_answer': '100',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of 11 * 11?',
                'option_1': '111',
                'option_2': '121',
                'option_3': '131',
                'option_4': '141',
                'correct_answer': '121',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is 49 ÷ 7?',
                'option_1': '5',
                'option_2': '6',
                'option_3': '7',
                'option_4': '8',
                'correct_answer': '7',
                'level': 3,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the square of 11?',
                'option_1': '100',
                'option_2': '110',
                'option_3': '121',
                'option_4': '144',
                'correct_answer': '121',
                'level': 3,
                'subject': 'Mathematics'
            },
            # Level 4
            {
                'question_text': 'What is the derivative of sin(x) with respect to x?',
                'option_1': 'cos(x)',
                'option_2': '-cos(x)',
                'option_3': '-sin(x)',
                'option_4': 'sin(x)',
                'correct_answer': 'cos(x)',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the area of a circle with a radius of r?',
                'option_1': '2πr',
                'option_2': 'πr^2',
                'option_3': 'πr',
                'option_4': 'r^2',
                'correct_answer': 'πr^2',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of the integral ∫ x^2 dx?',
                'option_1': 'x^3/3 + C',
                'option_2': 'x^3/2 + C',
                'option_3': '2x^3/3 + C',
                'option_4': 'x^3 + C',
                'correct_answer': 'x^3/3 + C',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'If a triangle has sides of lengths 3, 4, and 5, what is the area of the triangle?',
                'option_1': '12',
                'option_2': '6',
                'option_3': '9',
                'option_4': '10',
                'correct_answer': '6',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of the first 100 natural numbers?',
                'option_1': '5000',
                'option_2': '5050',
                'option_3': '4950',
                'option_4': '10050',
                'correct_answer': '5050',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the quadratic formula for the roots of ax^2 + bx + c = 0?',
                'option_1': '(-b ± √(b^2 - 4ac)) / 2a',
                'option_2': '(-b ± √(b^2 + 4ac)) / 2a',
                'option_3': '(b ± √(b^2 - 4ac)) / 2a',
                'option_4': '(b ± √(b^2 + 4ac)) / 2a',
                'correct_answer': '(-b ± √(b^2 - 4ac)) / 2a',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the equation of a line with slope m and y-intercept b?',
                'option_1': 'y = mx + b',
                'option_2': 'y = m/b + x',
                'option_3': 'y = m/x + b',
                'option_4': 'y = b/mx',
                'correct_answer': 'y = mx + b',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of the determinant of a 2x2 matrix [[a, b], [c, d]]?',
                'option_1': 'ad - bc',
                'option_2': 'ab - cd',
                'option_3': 'ac - bd',
                'option_4': 'ad + bc',
                'correct_answer': 'ad - bc',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of the interior angles of a hexagon?',
                'option_1': '360°',
                'option_2': '540°',
                'option_3': '720°',
                'option_4': '900°',
                'correct_answer': '720°',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the standard deviation a measure of?',
                'option_1': 'Central tendency',
                'option_2': 'Dispersion',
                'option_3': 'Skewness',
                'option_4': 'Kurtosis',
                'correct_answer': 'Dispersion',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'Which of the following is a prime number?',
                'option_1': '51',
                'option_2': '57',
                'option_3': '61',
                'option_4': '63',
                'correct_answer': '61',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the slope of the line perpendicular to y = 3x + 7?',
                'option_1': '3',
                'option_2': '-1/3',
                'option_3': '1/3',
                'option_4': '-3',
                'correct_answer': '-1/3',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of the exterior angles of any polygon?',
                'option_1': '180°',
                'option_2': '360°',
                'option_3': '540°',
                'option_4': '720°',
                'correct_answer': '360°',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the inverse of the function f(x) = 3x + 5?',
                'option_1': 'f^-1(x) = (x - 5)/3',
                'option_2': 'f^-1(x) = (x + 5)/3',
                'option_3': 'f^-1(x) = 3(x - 5)',
                'option_4': 'f^-1(x) = (x - 3)/5',
                'correct_answer': 'f^-1(x) = (x - 5)/3',
                'level': 4,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of the first n terms of an arithmetic sequence?',
                'option_1': 'n/2 * (a + l)',
                'option_2': 'n/2 * (a - l)',
                'option_3': 'n/2 * (a * l)',
                'option_4': 'n/2 * (a / l)',
                'correct_answer': 'n/2 * (a + l)',
                'level': 4,
                'subject': 'Mathematics'
            },
            # Level 5
            {
                'question_text': 'What is the derivative of sin(x) with respect to x?',
                'option_1': 'cos(x)',
                'option_2': '-cos(x)',
                'option_3': 'sin(x)',
                'option_4': '-sin(x)',
                'correct_answer': 'cos(x)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the integral of 1/x dx?',
                'option_1': 'ln|x| + C',
                'option_2': 'e^x + C',
                'option_3': 'x^2/2 + C',
                'option_4': '1/x + C',
                'correct_answer': 'ln|x| + C',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the solution to the quadratic equation x^2 - 4x + 4 = 0?',
                'option_1': 'x = 2',
                'option_2': 'x = -2',
                'option_3': 'x = 4',
                'option_4': 'x = 0',
                'correct_answer': 'x = 2',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the area of a circle with radius r?',
                'option_1': 'πr^2',
                'option_2': '2πr',
                'option_3': 'πd',
                'option_4': '2πr^2',
                'correct_answer': 'πr^2',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the volume of a sphere with radius r?',
                'option_1': '4/3πr^3',
                'option_2': '4πr^2',
                'option_3': 'πr^3',
                'option_4': '2/3πr^3',
                'correct_answer': '4/3πr^3',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the value of the limit lim(x→0) (sin(x)/x)?',
                'option_1': '1',
                'option_2': '0',
                'option_3': '∞',
                'option_4': '-1',
                'correct_answer': '1',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the sum of the first n terms of an arithmetic series?',
                'option_1': 'n/2 * (2a + (n - 1)d)',
                'option_2': 'n * (a + d)',
                'option_3': 'n * a',
                'option_4': 'n/2 * (a + d)',
                'correct_answer': 'n/2 * (2a + (n - 1)d)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the formula for the binomial expansion of (a + b)^n?',
                'option_1': 'Σ (nCk) a^(n-k) b^k',
                'option_2': 'a^n + b^n',
                'option_3': 'a^n + b^n + n!',
                'option_4': 'a^(n-1) + b^(n-1)',
                'correct_answer': 'Σ (nCk) a^(n-k) b^k',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the eigenvalue equation for a matrix A?',
                'option_1': 'A v = λ v',
                'option_2': 'A v = v λ',
                'option_3': 'A = λ v',
                'option_4': 'λ A = v',
                'correct_answer': 'A v = λ v',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the Pythagorean theorem?',
                'option_1': 'a^2 + b^2 = c^2',
                'option_2': 'a + b = c',
                'option_3': 'a^2 = b^2 + c^2',
                'option_4': 'a + b^2 = c',
                'correct_answer': 'a^2 + b^2 = c^2',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the characteristic equation of a 2x2 matrix?',
                'option_1': 'det(A - λI) = 0',
                'option_2': 'det(A) = 0',
                'option_3': 'trace(A) = λ',
                'option_4': 'A^2 = I',
                'correct_answer': 'det(A - λI) = 0',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the fundamental theorem of calculus?',
                'option_1': 'It relates differentiation and integration',
                'option_2': 'It states that all functions are integrable',
                'option_3': 'It describes the properties of differential equations',
                'option_4': 'It states that every function is continuous',
                'correct_answer': 'It relates differentiation and integration',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the distance formula in a 2D plane?',
                'option_1': '√((x2 - x1)^2 + (y2 - y1)^2)',
                'option_2': '√((x2 + x1)^2 + (y2 + y1)^2)',
                'option_3': '√((x2 - x1) + (y2 - y1))',
                'option_4': '√((x2 - x1)^2 - (y2 - y1)^2)',
                'correct_answer': '√((x2 - x1)^2 + (y2 - y1)^2)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the formula for the surface area of a cylinder?',
                'option_1': '2πr(h + r)',
                'option_2': '2πr^2 + 2πrh',
                'option_3': 'πr^2h',
                'option_4': '2πr^2',
                'correct_answer': '2πr(h + r)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the law of cosines?',
                'option_1': 'c^2 = a^2 + b^2 - 2ab cos(C)',
                'option_2': 'a^2 = b^2 + c^2 - 2bc cos(A)',
                'option_3': 'a^2 + b^2 = c^2',
                'option_4': 'a^2 = b^2 + c^2',
                'correct_answer': 'c^2 = a^2 + b^2 - 2ab cos(C)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the general solution to the differential equation dy/dx = ky?',
                'option_1': 'y = Ce^(kx)',
                'option_2': 'y = Ce^(-kx)',
                'option_3': 'y = Cx^k',
                'option_4': 'y = C/x',
                'correct_answer': 'y = Ce^(kx)',
                'level': 5,
                'subject': 'Mathematics'
            },
            {
                'question_text': 'What is the Laplace transform of δ(t)?',
                'option_1': '1',
                'option_2': '0',
                'option_3': 'e^(-st)',
                'option_4': 't',
                'correct_answer': '1',
                'level': 5,
                'subject': 'Mathematics'
            }
        ]
        
        # Add Questions to Database
        for q in questions:
            level = Level.objects.get(name=levels[q['level']])
            subject = Subject.objects.get(name=q['subject'])
            Question.objects.get_or_create(
                question_text=q['question_text'],
                option_1=q['option_1'],
                option_2=q['option_2'],
                option_3=q['option_3'],
                option_4=q['option_4'],
                correct_answer=q['correct_answer'],
                level=level,
                subject=subject
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated questions.'))
