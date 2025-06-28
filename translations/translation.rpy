init -3 python:
    LANG_ENG = "english"
    LANG_ESP = "spanish"
    LANG_FRE = "french"

    # Langue par défaut
    _selected_language = LANG_FRE

    def set_language(lang):
        global _selected_language
        _selected_language = lang
        persistent.selected_language = lang

    def get_language():
        return _selected_language

    languages = [LANG_ENG, LANG_ESP, LANG_FRE]

    class EvolvedString:
        def __init__(self, values, prefix=""):
            self.values = values
            self.prefix = prefix

        def _get_unique(self):
            return self.prefix + self.values.get(LANG_ENG, "")

        def __str__(self):
            lang = get_language()
            value = self.values.get(lang, self.values.get(LANG_ENG, ""))
            return self.prefix + value

        def __eq__(self, other):
            return other == self._get_unique() or other == str(self)

        def __hash__(self):
            return hash(self._get_unique())

        def __iter__(self):
            return iter(str(self))

        def __getitem__(self, item):
            return self._get_unique()[item]

        def __contains__(self, item):
            return item in str(self)

        def __lt__(self, other):
            return self._get_unique() < other

        def __le__(self, other):
            return self._get_unique() <= other

        def __gt__(self, other):
            return self._get_unique() > other

        def __ge__(self, other):
            return self._get_unique() >= other

        def __getstate__(self):
            return self._get_unique()

        def __setstate__(self, state):
            if isinstance(state, str):
                self.values = {LANG_ENG: state}
                self.prefix = ""
            else:
                self.__dict__.update(state)

        def __getattr__(self, name):
            raise AttributeError(f"'EvolvedString' object has no attribute '{name}'")

        def __add__(self, other):
            return str(self) + other

        def __radd__(self, other):
            return other + str(self)

        def split(self, value):
            return self._get_unique().split(value)

        def replace(self, value_original, value_replace):
            new_prefix = self.prefix.replace(value_original, value_replace)
            return EvolvedString(self.values, prefix=new_prefix)

        def index(self, value):
            return self._get_unique().index(value)

        def to_scene_text(self, map):
            text = str(self)
            text = text.replace("{", "#+#").replace("}", "#-#")
            text = text.replace("[", "{").replace("]", "}")
            text = text.format_map(map)
            text = text.replace("#+#", "{").replace("#-#", "}")
            return text

init -2 python:
    # Au lancement du jeu, charge la langue persistante si elle existe
    if hasattr(persistent, "selected_language") and persistent.selected_language in languages:
        set_language(persistent.selected_language)
    else:
        set_language(LANG_FRE)

define config.default_language = LANG_FRE
define config.enable_language_autodetect = True

init +1 python hide:
    config.developer = True
    config.console = True

init 999 screen navigation():

    modal True

    imagemap:
        ground "imagemaps/Nav_Menu_Ground.webp"
        idle "imagemaps/Nav_Menu_Idle.webp"
        hover "imagemaps/Nav_Menu_Hover.webp"
        selected_idle "imagemaps/Nav_Menu_Selected.webp"
        selected_hover "imagemaps/Nav_Menu_Selected.webp"
        
        hotspot (30, 240, 93, 25) action Preference("display", "any window")
        hotspot (162, 240, 115, 25) action Preference("display", "fullscreen")
        
        hotspot (28, 386, 50, 25) action Preference("text speed", 30)
        hotspot (112, 386, 72, 25) action Preference("text speed", 60)
        hotspot (222, 386, 50, 25) action Preference("text speed", 90)
        
        hotspot (28, 527, 50, 25) action SetField(config,"skip_delay",500)
        hotspot (112, 527, 72, 25) action SetField(config,"skip_delay",100)
        hotspot (222, 527, 50, 25) action SetField(config,"skip_delay",10)
        
        hotspot (101, 1018, 86, 31) action Hide("navigation", transition=dissolve)

        bar pos (141, 720) value Preference("music volume") style "pref_slider"
        bar pos (141, 808) value Preference("sound volume") style "pref_slider"
    
    vbox:
        xpos 25
        ypos 570
        textbutton "{b}Profanity: " + ("On" if profanity else "Off") + "{/b}" action ToggleVariable("profanity") text_font "fonts/pkmndp.ttf" text_color "#000" text_hover_color "#ff0000"
        textbutton "{b}Skip: " + ("All" if preferences.skip_unseen else "Seen") + "{/b}" action ToggleVariable("preferences.skip_unseen") text_font "fonts/pkmndp.ttf" text_color "#000" text_hover_color "#ff0000"
        null height 180
        textbutton "{b}Low-Specs: " + ("On" if lowspecs else "Off") + "{/b}" action ToggleVariable("lowspecs") text_font "fonts/pkmndp.ttf" text_color "#000" text_hover_color "#ff0000"
        null height 80

    vbox:
        xpos 25
        ypos 880
        style_prefix "radio"
        textbutton "{b}--------------{/b}" text_font "fonts/pkmndp.ttf" text_size 35 text_color "#000" text_hover_color "#ff0000"

        null height -20

        hbox:
            spacing 1
            textbutton "{b}English{/b}" action Function(set_language, LANG_ENG) text_font "fonts/pkmndp.ttf" text_size 30 text_color "#000" text_hover_color "#ff0000"
            textbutton "{b}|{/b}" text_font "fonts/pkmndp.ttf" text_size 25 text_color "#000" text_hover_color "#ff0000"
            textbutton "{b}Spanish{/b}" action Function(set_language, LANG_ESP) text_font "fonts/pkmndp.ttf" text_size 30 text_color "#000" text_hover_color "#ff0000"

        null height -5

        hbox:
            textbutton "{b}French{/b}" action Function(set_language, LANG_FRE) text_font "fonts/pkmndp.ttf" text_size 30 text_color "#000" text_hover_color "#ff0000"
