# Macro Guide for World of Warcraft

This World of Warcraft guide covers the basics of macros, how to access the Macro functions, and how to start creating your own macros! We also list the most popular macro constructions so you can build your own advanced macros^[[103;9u.

## What are Macros?

The Macro system is a tool that has been present in World of Warcraft since its inception. The base concept of a macro is to perform more than one action at a time to accomplish a task more quickly and easily. All macro commands start with a forward slash ( / ) to separate them from normal text actions. In this guide, we will go over the basics of macros and how to start creating your own! We also list the most popular macro constructions so you can build your own advanced macros. Macros fill many different commands and functions, including but not limited to emotes, spell casts, UI calls, and addon functions. However, there are limitations.
* Macros cannot use tools not normally accessible to players.
* Macros can only trigger one global cooldown. When the global cooldown is triggered, it cancels the remainder of the macro.
* Macros cannot be programmed to make decisions for the player, like \"heal the target with least HP\".

## Accessing the Macro Screen

Macros have a screen dedicated to themselves. This screen is accessible two ways:
* Open the Game Menu (Shortcut Esc) and then select Macros.
* Type /macro in the chat box and hitting Enter.

All macros you create are saved in Blizzard's server and are bound to your account or character, meaning you can access it from different computers and still retain all macros created. At any given time, an account might have 120 macros saved, plus 18 macros saved for each character. Account macros, as the name indicates, are shared by all your characters, while character ones aren't visible by other characters in your account once saved.

## Creating a Macro

To create a macro, enter the Macro Screen, then press the New button. By doing so you open a new window in which you must name your macro and select an icon for it. You can select any icon from the icons present in the game. Some macro directives that we will cover below allow you to override both name and icon shown by the macro, so you don't need to spend a lot of time picking either. You can name every macro just with a blank space and have the icon be the default question mark without any problems, but it's better to give them a short name and appropriate icon to identify them easily. Renaming a macro is easy -- just select it in your macro list and click on Change Name/Icon After selecting a name and an icon, you can drag the macro from the Macro Screen to your action bars to use it when you hit a keybind just like a normal spell. The next step is to write your macro.

## Writing Your First Macro

Announce a Cast One of the most basic macros you can write is to announce which spell you are using, which can be useful for interrupts. This can be written as follows: /say I'm casting Mind Blast /cast Mind Blast Cast and Cancel Another useful macro can be both to cast a spell and cancel it with the same button. This is normally used with defensive spells like Ice Block or Dispersion that reduce or remove your ability to deal damage. Hitting the macro button once will cast the spell, hitting it again will cancel it. Just don't spam that button or you may cancel it immediately after the cast! /cancelaura Ice Block /cast Ice Block Cast on Focus Another useful macro is to cast a certain spell only on a given target. For instance, you may want to damage one main target and interrupt another. For that, you can set this interrupt target on Focus, by typing /focus while targeting that target (which can also be accomplished by a macro!). Then you can write the macro as follows: /cast Kick

## Most Popular Macro Slash Commands and Modifiers

Here you will find a list of the most popular slash commands supported for macros and their functions. Macro Tip: A little trick you can do is to add #showtooltip to the start of a macro to have the macro behave as if it was the ability from the spellbook itself, overriding names and adding result spell's tooltip shown in the macro.

## Chat/Emote Macro Commands

These commands do not perform any actions; these are only for cosmetic purposes. Command Function /e or /emote Prints a message as if your character had emoted it /s or say Your character will say the message after the command

## Combat Macro Commands

These commands execute actions that are used mostly in combat-focused macros. Command Function /stopcasting Immediately stops your current spell cast or channel, if happening /targetlasttarget Changes your target to the last unit you had targeted /cast Casts the spell with the name input after it from your spell book. (i.e. /cast Fireball ) Using /cast Modifiers You can also have modifiers on spell casts that will appear between the /cast command and the spell name within brackets ( Kick. You can have multiple conditional modifiers linked by commas (,). All conditions need all to be true to happen, or have different groups of modifiers in different brackets. For instance, the following macro will cast the Fireball at your focus target if it exists, if it isn't dead and it is an enemy./ Otherwise the cast will happen on your current target. /cast

## Available Target Modifiers

Adding a target modifier to your macro will change your current target to the one specified if its conditional is true. @ (read 'at') can be replaced by target= in every command. Below you'll find a toggler containing a list of available Target Modifiers. Command Function @arena1 Targets the first unit in the Arena frames. This is a PvP-only modifier, usually only available during arena matches. There are more variants like arena2, arena3, etc. @boss1 Targets the first unit in the Boss frames. Usually only available during Dungeon and Raid encounters. There are more variants like boss2, boss3, etc. @cursor Targets the spell in the terrain the mouse is currently hovering (only available for spells with reticle targeting, like Mass Dispel or Blizzard). @focus Targets the focus target. @mouseover Targets the spell on the target that the mouse is currently hovering. @pet Target the player's pet. @player Targets the player. @target Targets the player's current target. @targettarget Targets the target's target. For instance, when used targeting a Boss, it will target the tank or whoever the boss has targeted in that instant.

## Available Conditional Modifiers

All these conditionals can be used to decide which action to be taken. You can add no in front of all of them to have them have them behave the exact opposite. For instance, noharm is true for any target that isn't an enemy, but that could include targets that you can't help, like neutral NPCs. Command Function advflyable true if you are currently somewhere you can skyride. button:number (or btn) used to check with which mouse button you activated the macro. is the default, left button, right, middle. For mouses with more buttons the number of them button follows the pattern for the option. channeling true if you are currently channeling a spell. combat true if you're in combat. dead true if the target for the cast is dead. equipped:slot (or worn) true if you have an item equipped in the slot. For instance, will be true if you have a chest piece equipped. exists true if the target for the cast exists. flyable true if you are currently somewhere you can fly. flying true if you are currently flying. form:number or stance:number true if the character is currently in the given form/stance of a given id. List below. group true if you are currently in a group. Can be specialized to or . harm true if the target for the cast is an enemy. help true if you can aid the target for the cast. indoors true if you are currently in a position that is considered indoors. known:spellID or known:spellName Used to check if your character knows how to cast a certain spell. Useful for macros that should change depending on talents learned mounted true if you are currently mounted. outdoors true if you are currently in a position that is considered outdoors. pet true if the player has a current pet. petbattle true if you are in a pet battle pvpcombat true if you can use PvP Talents. resting true if you're in a rested area like a city or an inn. spec:number true if you're currently in the specialization given by the number. Specializations are ordered in alphabetical order and can be checked in the Specializations Menu. swimming true if you are currently swimming. List of Forms per Class * [Druid](https://www.wowhead.com/class=11/druid) 1. [Bear Form](https://www.wowhead.com/spell=5487/bear-form) 2. [Cat Form](https://www.wowhead.com/spell=768/cat-form) 3. [Travel Form](https://www.wowhead.com/spell=783/travel-form)/[Aquatic Form](https://www.wowhead.com/spell=276012/aquatic-form)/[Flight Form](https://www.wowhead.com/spell=165962/flight-form) 4. [Moonkin Form](https://www.wowhead.com/spell=24858/moonkin-form) 5. [Treant Form](https://www.wowhead.com/spell=114282/treant-form) If you don't have Moonkin Form learned, Treant form will return \"4\" instead * [Priest](https://www.wowhead.com/class=5/priest) 1. [Shadowform](https://www.wowhead.com/spell=232698/shadowform) * [Rogue](https://www.wowhead.com/class=4/rogue) 1. [Stealth](https://www.wowhead.com/spell=1784/stealth) 2. [Vanish](https://www.wowhead.com/spell=1856/vanish)/[Shadow Dance](https://www.wowhead.com/spell=185313/shadow-dance) (For Subtlety Rogues, all three return \"1\" instead). * [Shaman](https://www.wowhead.com/class=7/shaman) 1. [Ghost Wolf](https://www.wowhead.com/spell=2645/ghost-wolf) * [Warrior](https://www.wowhead.com/class=1/warrior) 1. [Battle Stance](https://www.wowhead.com/spell=386164/battle-stance) 2. [Defensive Stance](https://www.wowhead.com/spell=386208/defensive-stance) 3. [Berserker Stance](https://www.wowhead.com/spell=386196/berserker-stance)

## Key Modifiers

Command Function mod:shift true if the keybind was pressed while the SHIFT key was pressed. mod:alt true if the keybind was pressed while the ALT key was pressed. mod:ctrl true if the keybind was pressed while the CTRL key was pressed.

## General Commands

These commands can be used for both combat and non-combat situations. Command Function /run (or /script) Execute the message after it as a LUA script (scripting language present in WoW addons and scripts. /use uses the item with the name written after the command. Can also be used with numbers, which will cause it to use the item equipped in the slot of that number. (i.e. /use Potion of Prolonged Power or /use 14 to use your second trinket) * 1 - Head * 2 - Neck * 3 - Shoulder * 4 - Shirt * 5 - Chest * 6 - Waist * 7 - Legs * 8 - Feet * 9 - Wrist * 10 - Hands * 11 - Finger 1 * 12 - Finger 2 * 13 - Trinket 1 * 14 - Trinket 2 * 15 - Back * 16 - Main hand * 17 - Off hand * 19 - Tabard

## More Advanced Macro Guides

This guide covers the basics you need to know about to create your own macros, but, if you would like to read more about them, make sure to check out Adreaver's guide on the [Official WoW Forums](https://us.forums.blizzard.com/en/wow/t/macros-essential-information/21139). If you would like example of macros for your class, you can check Elvenbane's [post on the Official Forums](https://us.forums.blizzard.com/en/wow/t/macros-condensing-your-physical-keys/16422).

## Comments

Comment by mymy379

Excellent guide! All the basic info conveniently placed in 1 place (instead of digging through wowpedia pages like I normally do), in an easy to read format. Also, Macro Menu can be accessed with just '/m' for maximum lazyness :P Edit: Just noticed the guide is missing some specialized conditionals, full list can be found [here](https://wow.gamepedia.com/Macro_conditionals), in addition to links already present at the bottom of the guide. Edit2: WoWwiki moved, [here](https://warcraft.wiki.gg/wiki/Macro_conditionals) is far likelier to receive any further updates.

Comment by bleuwolfe

thank you thank you THANK YOU for this guide, you have no idea how long I've been wanting one so I can make up my own (working!) macros instead of having to search for someone else posting one for something I want to do. And anyone who's never tried a macro should really give it a spin, they make life so much easier :)

Comment by Aprune

Nice guide, but missing some elements : * Could explain the meaning of brackets, especially the consecutive ones. Same for the use of consecutive options, separated with a semicolon. * Missing the form condition, which is greatly useful for Druids (but for Shadow Priests too, and Warriors if stances are getting back) * One error though : pet - true if the player has no pet currently. should be the other way around.

Comment by Gothy

Saving this and coming back to it later. :D

Comment by Shurai

why no druid form's under conditions
?
Comment by 509794

/focus command does not work in the current Classic patch

Comment by Aerynsun8449

I have been trying to get the nodead to work with /target with no success. I've tried; /target Shadow Panther /target Shadow Panther /target Shadow Panther Everything I try targets the Shadow Panther I just killed. How do I get it to ignore the dead ones?

Comment by ArxonHavenloft

So is there a way in Classic to format a Talisman of Ephemeral Power macro in this manner:? -If Cooldown(TOEP) = 0 then /Use TOEP else /Cast ShadowBolt(Rank 9).

Comment by kelitaur

Can an \"instant\" from the Heart of Azeroth neck piece be macro'd?

Comment by EatFish

Hi Lovely guide I tried and tried.. but no cigar- Any chance anyone could help me out with a macro for my rouge=? I tried to make a countdown macro for using my Shroud of Concealment, but alas no luck. no problem in getting. /s Shroud up /cast Shroud of Concealment to work But I cannot get a countdown timer to say when shroud is running out. I do not want an addon for just this. In advance. Thanks for any help/suggestions

Comment by Boondoggles

/cast ' is doing. In another comment, someone asked about having multiple sets of brackets, semicolons, etc. I will try to explain that here: /use spell1; spell2;spell3;spell4 - In any set of 'conditions', you are looking at an all-or-nothing. In the case of 'moreconditions', spell2 will only be /used if ALL of the 'moreconditions' are met. - Inside a 'set of conditions'/square-brackets, you can view the commas as the word 'AND'. E.g. \"/use Rejuvenation\" essentially means \"use rejuvenation @ a-target-if-I-have-one AND I can help said target\" - However, spell1 has two sets of conditions, which is essentially two chances at an 'all-or-nothing', or in logical/coding terms, an 'or'. If either 'setofconditions' is evaluated to 'true', or 'anothersetofconditions' is evaluated to true, spell1 will be /used, otherwise, it will go on to check further into the macro - The semicolons can be largely viewed as 'else' or 'else if'... in the example above, the macro is going to always/eventually try 'else spell4' if all of the previous conditionals in the same line had failed tl;dr if there multiple sets of without semicolons before a spell/item/whatever name, it is saying if ANY of these are true, do the thing, otherwise a semicolon denotes an 'else' or 'else if', indicating a new set of evaluations will commence for the next (IF ANY!) conditions

Comment by Unaffiliated

(Tested 9.1 Shadowlands) on a hunch I tried and confirmed that there is currently a macro conditional for Warmode, but only as a generalised spec, so you can’t have it change automatically with your talent selections. /cast ability Also /cast ability I hope this helps anyone else searching for macro solutions.

Comment by alanwelch91

can you add a bit on castsequence macros?

Comment by RealRevChris

I do not know what Dragonflight has broken, but I can not get the /cast SPELL1, SPELL2, SPELL3, SPELL4 or &several others. The changes the macro button, but just shows a \"?\" & no spell. Anyone figure this out?

Comment by Kessyra

Can anyone help me. I would like both spells to work @mouseover but I'm not sure how to do this. This one doesn't work. Barbed shot will cast at mouseover but that overrides Kill Shot. Thank you /use Barbed Shot /castKill Shot

Comment by morituri

Please excuse my ignorance. Why many macros begin with the \"showtooltip\" line?

Comment by Raffo42

Something I just spent way too long on: When turning a targetable AoE into an instant @cursor, it of course works with /cast Ring of Peace It even works just like that with most modifiers: /cast Ring of Peace But sometimes, the cast with one specific modifier (for me it was alt) is cast @player, even tho the macro still says @cursor
