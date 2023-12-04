# Resources and themes

> Attention: the principle of operation may change during the active development of the project

<br>

## Description
To give your application the look you want, you can use design packages that use customizable cascading style sheet templates, icons, images, etc.

<br>

## Theme settings file
The `theme.json` file is used to customize the theme package, as well as to define fields and properties of templates, the data from which is processed in `ThemeManager` and passed to `template.qss`.

To define the type of design package, specify in the `theme.json` file the name of the design file - `{"theme": "theme.qss"}` or the template file - `{"template": "template.qss"}`.

<br>

## Theme template file
If you decide to use a design template, you are required to create the `template.qss` file and, using the fields labeled `theme.json`, write your design theme.

Example of using the design fields:

```css
QPushButton {
    color: @primaryFontColor100;
    background-color: @primaryBackgroundColor100;
    border-color: @buttonsBorderColor100;
    border-style: @buttonsBorderStyle;
    border-width: @buttonsBorderWidth;
}
```