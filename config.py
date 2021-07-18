import os
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List
from datetime import date

mod = "mod4"
ctrl = "control"
alt = 'mod1'
terminal = "alacritty"

keys = [
    # Default Configurations
    ## Switch between windows
    Key([mod], "h",     lazy.layout.left(),  desc="Move focus to left"),
    Key([mod], "l",     lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j",     lazy.layout.down(),  desc="Move focus down"),
    Key([mod], "k",     lazy.layout.up(),    desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),  desc="Move window focus to other window"),

    ## Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),   desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),   desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(),            desc="Reset all window sizes"),
    Key([mod, "control"], "z", lazy.spawn("dm-tool lock"),   desc="Grow window up"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal),                desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(),   desc="Kill focused window"),

    Key([mod, "control"], "p", lazy.restart(),  desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.spawn('rofi -show power-menu -modi power-menu:rofi-power-menu'), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),            desc="Spawn a command using a prompt widget"),

    #Rofi
    Key([mod], "space", lazy.spawn('rofi -show drun'), desc="Kill focused window"),
    Key([mod], "p", lazy.spawn('rofi -show run'),      desc="Kill focused window"),

    Key([mod], "F11", lazy.spawn('brightnessctl -d "intel_backlight" set 10%-'),      desc="Kill focused window"),
    Key([mod], "F12", lazy.spawn('brightnessctl -d "intel_backlight" set +10%'),      desc="Kill focused window"),
    Key([mod], "F2", lazy.spawn('pactl -- set-sink-volume 0 -10%'),      desc="Kill focused window"),
    Key([mod], "F3", lazy.spawn('pactl -- set-sink-volume 0 +10%'),      desc="Kill focused window"),
    Key([mod], "F1", lazy.spawn('pactl -- set-sink-volume 0 0'),      desc="Kill focused window"),

    KeyChord([mod], "s", [
        Key([], "f", lazy.spawn("bash /home/lenovo/.config/qtile/scripts/screenshot_full.sh")),
        Key([], "s", lazy.spawn("bash /home/lenovo/.config/qtile/scripts/screenshot_partial.sh"))
    ])
]

group_names = [("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'floating'}),
               ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": "8fbcbb",
                "border_normal": "2e3440"
                }

colors = [["#2e3440", "#2e3440"], # panel background
          ["#2e3440", "#2e3440"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#81a1c1", "#81a1c1"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#81a1c1", "#81a1c1"], # window name
          ["#81a1c1", "#81a1c1"]] # backbround for inactive screens

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Columns(border_focus_stack='#d75f5f'),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu Bold',
    fontsize=10,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    background = colors[0]),
                widget.GroupBox(
                   font = "Ubuntu Bold",
                    fontsize = 10,
                    margin_y = 4,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 2,
                    active = colors[2],
                    inactive = colors[7],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "line",
                    this_current_screen_border = colors[6],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[6],
                    other_screen_border = colors[4],
                    foreground = colors[2],
                    background = colors[0]),
                widget.Prompt(
                    foreground = colors[2],
                    background = colors[0]),
                widget.WindowName(
                    foreground = colors[2],
                    background = colors[0],
                    padding = 10,
                    margin = 5),
                widget.Chord(
                    chords_colors={'launch': ("#ff0000", "#ffffff"),},
                    name_transform=lambda name: name.upper(),
                    foreground = colors[2],
                    background = colors[0]),
                 widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = "#5e81ac",
                       padding = -12.5,
                       fontsize = 39
                       ), 
                widget.CurrentLayout(
                    foreground = colors[2],
                    background = "#5e81ac"),
                 widget.TextBox(
                       text = '',
                       background = "#5e81ac",
                       foreground = "#a3be8c",
                       padding = -12.5,
                       fontsize = 39
                       ), 
                widget.Clock(
                    format='%Y-%m-%d %a %I:%M %p',
                    foreground = colors[2],
                    background = "#a3be8c"),
                widget.TextBox(
                       text = '',
                       background = "#a3be8c",
                       foreground = "#bf616a",
                       padding = -12.5,
                       fontsize = 39
                       ),
                widget.TextBox(
                       text = 'Battery: ',
                       background = "#bf616a",
                       foreground = colors[2],
                       padding = 0,
                       ),
                widget.Battery(
                    update_interval=10,
                    format = '{percent:2.0%}',
                    foreground = colors[2],
                    background = "#bf616a"),
                widget.TextBox(
                       text = '',
                       background = "#bf616a",
                       foreground = "#4c566a",
                       padding = -12.5,
                       fontsize = 39
                       ),
                widget.Systray(
                    foreground = colors[2],
                    background = "#4c566a"),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    background = "#4c566a")
            ],
            22,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

wmname = "LG3D"
