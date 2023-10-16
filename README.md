# Battleship Game
![Website testing for responsiveness](assets/images/game_play.png)

This is quite simple but same very interesting game on terms of 
programing. 
I have implemented few features in this game:
- Game has some logic, so CPU is not just randomly shooting
- Player can change Map size
- Player can adjust fleet:
  - Add more ships
  - Modify existing ones
  - Delete ship
- If user wants, also can change coordinate system from digits to letters
- 
The aim of this project is to  present my skills on Python that i have 
acquired on Code Institute "Full Stack Development" course.

[Link to live page](https://tomosius.github.io/Vampyre/)

## Table of contents
- [VAMPIRES](#vampires)
  - [Table of contents](#table-of-contents)
  - [User Experience (UX)](#user-experience-ux)
    - [Website Aim](#website-aim)
    - [Stories](#stories)
  - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Images](#images)
  - [Features](#features)
    - [General Features](#general-features)
    - [Accessibility](#accessibility)
  - [Testing](#testing)
    - [Responsiveness](#responsiveness)
    - [Compatibility](#compatibility)
    - [W3C validation HTML](#w3c-validation-html)
    - [W3C validation CSS](#w3c-validation-css)
    - [404 Page](#404-page)
  - [Technologies](#technologies)
    - [Languages Used](#languages-used)
    - [Bootstrapping](#bootstrapping)
    - [Tools used](#tools-used)
  - [Acknowledgements](#acknowledgements)
## User Experience (UX)
### Website Aim
* This website is to represent world of "Vampires"
* Show how our perspective about them changed in timeline
* Give reader access to contact website designer
### Stories
* Brief history about Dracula
* First movie about Vampires
* Changing perspective about vampires
* Vampires in modern art

[Back to top ⇧](#rpsls)

## Design
### Color Scheme
* Website is based on these colors:
  - Blood RGB(136,8,8)
  - Black
  - White
  - Smoked-White (les vibrant white)
### Images
* All images are used from Internet with common or free user rights

[Back to top ⇧](#rpsls)

## Features
### General Features
* background: linear-gradient(to bottom, white, #880808):<br>
White color is changing to blood from top towards bottom of page, for this i have implemented
* article:nth-child(odd) > img <br>
aligning all articles images that are odd to be floating to right
* article:nth-child(even) > img<br>
aligning all articles images that are even to be floating to left
* @media screen and (max-width: 600px)<br>
Settings for website when used on small screen with resolution 600 pix and below
* Page Contact has inline styling as on some screens footer gets higher then bottom, as page is tiny, for this i used: style="height: 100vh;"
* Navigation bar has links to all pages: Home, Brief History, Contact
* Footer has links to Personal LinkedIn, Source Code and this README.md
* When hovering mouse above an Element, color changes
* Main page Intro text is placed on image with lighter background
* Same page on smaller screen sizes, that text moves above the picture
### Accessibility
* all links have 'aria-label' to ensure readability of the website
* all images have 'alt' attributes
* Headings elements 'h1', 'h2', 'h3' have been applied to convey structure

[Back to top ⇧](#rpsls)

## Testing
### Responsiveness
* All Pages have been tested with:<br> https://responsivedesignchecker.com
* Chrome DevTools were used to test website on various screen sizes
### Compatibility
Website was tested for appearance, functionality or responsiveness on these devices:
* Ipad Pro 12.9"
* Macbook Air 13"
* Iphone 12
All these devices have used Safari, Firefox and Google Chrome browsers
### Manual Testing
* Device compatibility

| Device | Test | Result |
| --- | --- | --- |
| MacBook Air 13" | No appearance, responsiveness nor functionality issues. | Pass |
| iPad Pro 12.9" | No appearance, responsiveness nor functionality issues. | Pass |
| iPhone 8 | No appearance, responsiveness nor functionality issues. | Pass |


* Browser Compatibility

| Browser | Test | Result  |
--- | --- | ---
Google Chrome | No appearance, responsiveness nor functionality issues.| Pass
Safari | No appearance, responsiveness nor functionality issues. | Pass
Mozilla Firefox | Scrollbar is visible even though it should be hidden. <br>No responsiveness nor functionality issues.| Pass
Microsoft Edge | No appearance, responsiveness nor functionality issues. | Pass

* Website Elements Testing

    - General

    | Feature | Test | Result |
    | --- | --- | --- |
    | Navigation Bar | Hover effect and links are working as expected. | Pass |
    | Social Links | Open the specific website on a new tab. | Pass |
    | Blood dripping animation | Animation is visible on all screen sizes | Pass |

    - Home Section
    
     |Feature | Test | Result |
    | --- | --- | --- |
    | Main intro text big screen | Text is visible on main image on high resolution screens| Pass |
    | Man intro text small screen | Text disappears on image and reappears above picture as intro text | Pass |
    
    - Contact Form 
    
    | Feature | Test | Result |
    | --- | --- | --- |
    | Form | Require all fields in the right format before submission. |  Pass |
    | Send Feedback Button | Hover effect work as expected and submit form when clicked. |  Pass |

    - Brief History  Section

    | Feature | Test | Result |
    | --- | --- | --- |
    | Images float to left or right | Images are automatically floating to left orr right depending on article (odd articles float right, even - left) | Pass |
    | Small screen images are not floating | Images stop floating to sides on smaller screens | Pass |

    - 404 Error Page

    | Feature | Test | Result |
    | --- | --- | --- |
    | 404 Error Page | Entering an incorrect address into the address bar bring the user to the 404 error page. | Pass |

[Back to top ⇧](#rpsls)

### W3C validation HTML
![W3C Index Page Validation](assets/images/w3c_index.png)
![W3C Brief Page Validation](assets/images/w3c_brief.png)
![W3C Contact Page Validation](assets/images/w3c_contact.png)
### W3C validation CSS
![W3C CSS file Validation](assets/images/w3c_css.png)
### 404 Page
If error occurs, website will redirect to 404 Page:
![404 website Page](assets/images/404_page_ss.png)

[Back to top ⇧](#rpsls)

## Technologies
### Languages Used
- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
### Bootstrapping
* Fonts were used from Google Fonts
* Icons were used from fontawesome
### Tools used
* Gimp for cropping  and adjusting images
* Visual Studio Code - as Code Editor
* Git / GitHub for Version Control
* Shields.io for badges used in README.md

[Back to top ⇧](#rpsls)

## Acknowledgements
* Idea and biggest support to my partner
* Code Institute for support and knowledge
* Tutor Marcel for guidance and feedback
* [W3Schools](https://www.w3schools.com) for information
* [Google](https://www.google.co.uk) for images, tips and tricks on HTML5 abd CSS

[Back to top ⇧](#rpsls)