# [[file:readme.org::*Skabelon som I skal arbejde videre ud fra][Skabelon som I skal arbejde videre ud fra:1]]
import arcade
import math

VINDUEBREDDE = 800
VINDUEHOEJDE = 600

BAGGRUNDSFARVE = arcade.color.DARK_GRAY

BATBREDDE = 100
BATHOEJDE = 10
BATFARVE = arcade.color.WHITE

BOLDRADIUS = 5
BOLDFARVE = arcade.color.RED
BOLDFART = 5

# Simpel klasse for en bold. Nedarver fra SpriteCircle,
# som har de samme egenskaber som en alm Sprite, men som ikke
# kraever en billedfil.
class Bold(arcade.SpriteCircle):
    def __init__(self, radius, farve, fart):
        super().__init__(radius, farve)
        self.fart = fart
        self.fri = False

    def nulstil(self, bat):
        self.fri = False
        self.center_x = bat.center_x
        self.bottom = bat.top
        self.stop()


# Simpel klasse for battet. Nedarver fra SpriteSolidColor,
# som har de samme egenskaber som en alm Sprite. Her er det
# bare et rektangel i stedet for et billede, der vises.
class Bat(arcade.SpriteSolidColor):
    def __init__(self, bredde, hoejde, farve):
        super().__init__(bredde, hoejde, farve)

    def nulstil(self):
        self.center_x = VINDUEBREDDE / 2
        self.bottom = 0


# Denne klasse skal repraesentere de klodser, som man skal ramme med bolden.
# Man kan med fordel opbygge nye klasser for mere anvancerede klodser, ved at lade
# dem nedarve fra denne.
class SimpelKlods(arcade.SpriteSolidColor):
    def __init__(self, bredde, hoejde, farve, hits_tilbage=1):
        super().__init__(bredde, hoejde, farve)
        self.hits_tilbage = hits_tilbage


# Denne klasse skal bruges til at tegne et gennemsigtigt "overlay" over hver bane,
# inden banen starter rigtigt."
class BaneIntroduktionView(arcade.View):
    def __init__(self, tilhoerende_bane_view):
        super().__init__()
        # "link" tilbage til den rigtige bane.
        self.tilhoerende_bane_view = tilhoerende_bane_view

    def on_draw(self):
        self.clear()
        # Tegner den bagvedliggende bane op
        self.tilhoerende_bane_view.on_draw()

        # Tegner en gennemsigtig firkant over hele vinduet.
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=self.window.width,
            top=self.window.height,
            bottom=0,
            color=arcade.color.WHITE + (100,),
            # + (100,) soerger for at den farve er transparent
        )
        # Generel banetekst med banenummer etc
        banetekst = arcade.Text(
            text=f"Bane {self.tilhoerende_bane_view.banenummer if self.tilhoerende_bane_view.banenummer else ''}",
            start_x=self.window.width / 2,
            start_y=self.window.height * 2 / 3,
            color=arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        banetekst.draw()
        # Instruktionstekst - tryk på en af tasterne på musen
        instruktionstekst = arcade.Text(
            text="Tryk på en af musen knapper for at begynde.",
            start_x=self.window.width / 2,
            start_y=self.window.height * 1 / 3,
            color=arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        instruktionstekst.draw()

    def on_mouse_press(self, _x, _y, _tast, _modifikationstast):
        # Viser den rigtige bane.
        self.window.show_view(self.tilhoerende_bane_view)


# En klasse for en tom bane uden klodser i.
# Den skal bruges til at samle al logik, som skal vaere faelles for
# alle baner i spillet.
class TomBaneView(arcade.View):
    def __init__(self, liv_tilbage, banenummer=None):
        super().__init__()
        self.banenummer = banenummer
        self.liv_tilbage = liv_tilbage
        self.bat_liste = None
        self.bold_liste = None
        self.klodser_liste = None
        self.bane_introduktion_view = None

    def setup(self):
        arcade.set_background_color(BAGGRUNDSFARVE)
        self.bat_liste = arcade.SpriteList()
        self.bat = Bat(BATBREDDE, BATHOEJDE, BATFARVE)
        self.bat.nulstil()
        self.bat_liste.append(self.bat)

        self.bold_liste = arcade.SpriteList()
        self.bold = Bold(BOLDRADIUS, BOLDFARVE, BOLDFART)
        self.bold.nulstil(self.bat)
        self.bold_liste.append(self.bold)

        self.klodser_liste = arcade.SpriteList()
        self.klodser_setup()

        self.bane_introduktion_view = BaneIntroduktionView(self)
        self.window.show_view(self.bane_introduktion_view)

    def klodser_setup(self):
        """Opbyg jeres bane ved at aendre på/overskrive koden i denne funktion."""
        # Erstat pass med jeres egen kode. Goer det kun for kode, som skal vaere
        # faelles for ALLE baner.
        pass

    def nulstil(self):
        # Nulstiller battet og bolden til midt nederst paa skaermen.
        self.bat.nulstil()
        self.bold.nulstil(self.bat)

    def on_update(self, delta_tid):
        # Opdaterer bolden i boldlisten
        self.bold_liste.update()

        # Kollision mellem vinduets sider og bolden
        # Herunder skal I indsaette jeres kode for at lade bolden blive inden for
        # vinduet.

        # Kollision mellem bold og klodser
        # Opbygger en liste med alle de klodser, bolden rammer
        ramte_klodser_liste = arcade.check_for_collision_with_list(
            self.bold, self.klodser_liste
        )

        # Her skal logikken vaere for kollision mellem bold og en enkelt klods
        # Erstat pass med jeres egen kode for logikken.
        for klods in ramte_klodser_liste:
            pass

        # Kollision mellem bold og bat
        if arcade.check_for_collision(self.bold, self.bat):
            # Herunder skal I indsaette jeres logik for kollision mellem bold og bat.
            # Fjern pass og erstat det med jeres egen kode.
            pass

        # Mist liv og tjek for game over
        if self.bold.top < 0:
            self.liv_tilbage -= 1
            if self.liv_tilbage < 1:
                # Erstat med kode, som viser en game overskaerm
                print("Game over")
            self.nulstil()

        # Til naeste bane
        if self.liv_tilbage > 0 and not self.klodser_liste:
            self.til_naeste_bane_view()

    def til_naeste_bane_view(self):
        """Denne metode skal overskrives i en underklasse. Opret ny bane-objekt og soerg for at koere setup af denne ogsaa."""
        pass

    def on_draw(self):
        self.clear()
        self.bat_liste.draw()
        self.bold_liste.draw()
        self.klodser_liste.draw()
        # Hvis der skal skrives, hvor mange liv der er tilbage, eller hvad
        # en score er, saa skal koden til det staa herunder i denne metode.

    def on_mouse_motion(self, x, y, hastighed_x, hastighed_y):
        # Battet flytter sig efter musen
        # Hvis man vil soerge for at hele battet ikke kan komme uden for vinduet,
        # er det typisk i denne metode, at koden skal soerge for det.
        self.bat.center_x = x
        if not self.bold.fri:
            self.bold.center_x = self.bat.center_x

    def on_mouse_press(self, _x, _y, _tast, _modifikationstast):
        # Bolden sendes afsted fra battet ved at trykke paa en vilkaarlig tast
        # paa musen.
        # Lige nu sendes bolden afsted med 45 grader mod hoejre fra battet
        # Aendr koden, saa afsending af bolden foregaar, som I oensker det.
        if not self.bold.fri:
            self.bold.fri = True
            self.bold.change_y = math.sin(math.pi / 4) * BOLDFART
            self.bold.change_x = math.cos(math.pi / 4) * BOLDFART

    def on_key_press(self, tast, modifikationstast):
        # I denne metode skal I skrive jeres kode, som skal holde styr paa
        # tastetryk. F.eks. hvis man vil lukke spillet ved at trykke paa Q
        pass


# Her oprettes foerste bane.
# Den nedarver fra TomBaneView, saa det er kun de to viste metoder,
# som skal overskrives for at passe til netop bane 1
class Bane1View(TomBaneView):
    def klodser_setup(self):
        # Opbyg jeres egen bane
        klods = SimpelKlods(100, 50, arcade.color.FLUORESCENT_YELLOW, hits_tilbage=1)
        klods.center_x = self.window.width / 2
        klods.center_y = self.window.height / 2
        self.klodser_liste.append(klods)

    def til_naeste_bane_view(self):
        bane_2_view = Bane2View(self.liv_tilbage, banenummer=2)
        bane_2_view.setup()


# Klasse for bane nummer 2
class Bane2View(TomBaneView):
    def klodser_setup(self):
        # Opbyg jeres egen bane
        pass

    def til_naeste_bane_view(self):
        # Opret baneobjekt og husk at koere setup for denne efterfølgende.
        pass


# Herunder skal I self oprette klasser for alle de andre baner, som I vil have
# med i jeres spil.
# Se paa eksemplet med Bane1View og hvordan den linker til bane 2


# Velkomstklassen, som viser en velkomstskaerm
class VelkomstView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.HONEYDEW)

    def on_draw(self):
        self.clear()
        tekst = arcade.Text(
            text="Velkommen til Arkanoid",
            start_x=self.window.width / 2,
            start_y=self.window.height * 2 / 3,
            color=arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        tekst.draw()
        # Hvis der skal vaere instruktioner til spilleren, saa
        # kan koden til dem skrives herunder

    def on_mouse_press(self, _x, _y, _tast, _modifikationstast):
        # Foerste bane startes, naar man trykker paa en tast paa musen.
        bane_1_view = Bane1View(liv_tilbage=3, banenummer=1)
        bane_1_view.setup()


# Denne klasse skal bruges til at opbygge en eventuelt pauseskaerm
# Se paa opbygningen af BaneIntroduktionView-klassen for inspiration
class PauseView(arcade.View):
    pass


# Denne klasse skal bruges til at opbygge en eventuelt game over-klasse, som kan
# vises, hvis man mister alle liv, inden man har gennemfoert alle baner.
# Se paa opbygningen af BaneIntroduktionView-klassen for inspiration
class GameOverView(arcade.View):
    pass


# Denne klasse skal bruges til at opbygge en eventuelt klasse til at vise, at
# man har gennemfoert spillet
# Se paa opbygningen af BaneIntroduktionView-klassen for inspiration
class GennemfoertView(arcade.View):
    pass


def main():
    break_out_vindue = arcade.Window(VINDUEBREDDE, VINDUEHOEJDE, "Arkanoid!")

    velkomst_view = VelkomstView()
    break_out_vindue.show_view(velkomst_view)

    arcade.run()


main()
# Skabelon som I skal arbejde videre ud fra:1 ends here
