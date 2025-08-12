# Capstone Project

## Chaos Cards | Full Stack Web Application

![Website Mockups](docs/design/website-mockup.png)

**Author:** James Jarvis-Bicknell

**This project was developed as part of my 16-week full-stack software development bootcamp with Code Institute. It brings together what we have learned: front-end (HTML, CSS, Bootstrap, JavaScript) and back-end (Python, Django).**

## Introduction

**Chaos Cards**

*Chaos Cards* is a Django-powered web application designed to inject unpredictability into daily life.

It allows users to create, edit, delete, and spin random “chaos cards” — each containing an activity or challenge.

The project was built as a full-stack application with the aim of:

- Encouraging spontaneity and playfulness
- Demonstrating CRUD (Create, Read, Update, Delete) functionality
- Exploring user authentication and personalized content
- Providing a responsive, accessible, and engaging user experience

**Intended Audience:**

Anyone looking to break free from routine — from thrill-seekers to bored office workers, procrastinators, creatives, and people simply wanting something new to do.

**Core Functionality**

- User registration and login/logout
- Creating, reading, editing, and deleting personal chaos cards
- Viewing all personal cards
- Spinning a virtual “wheel of chaos” to select a random card
- Contact/feedback submission form

**Technologies Used:**

- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript (ES6)
- Backend: Python 3, Django 5
- Database: PostgreSQL
- Hosting: Heroku
- Static & Media Storage: Cloudinary
- Version Control: Git & GitHub

Click link to see [**live project**](https://chaos-cards-de954de9fb2a.herokuapp.com/)

## Table of Contents:

1. [Introduction](#introduction)
2. [UX Design](#ux-design)
    - [Design Rationale](#design-rationale)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
    - [Database Design](#database-design)
3. [Agile Working](#agile-working)
4. [Key Features](#key-features)
5. [Deployment](#deployment)
6. [AI Implementation](#ai-implementation)
7. [Testing](#testing)
8. [Future Enhancements](#future-enhancements)
9. [Credits](#credits)

## UX Design:

### Design Rationale

- **Layout:**

    Built for clarity and responsiveness. Navigation is persistent across pages, with clear CTAs for logging in, creating cards, and spinning the chaos wheel.
- **Colour Scheme:**

    ![Colour Palette](docs/design/colour-palette.png)

    A vibrant yet minimal palette to balance playful chaos with readability. Bright accent colours highlight interactive elements. Dark green was chosen as the dominant background color as it was evocative of 'games' tables, gambling and chance - which was the theme of the website.
- **Typography:**

    Clean, legible sans-serif fonts with varying weights for hierarchy.
- **Accessibility:**

    - Semantic HTML
    - ARIA labels for interactive components
    - Sufficient colour contrast
    - Fully responsive design for mobile, tablet and desktop
- **Images:**

    - Default images were AI generated using [Microsoft Copilot](https://copilot.microsoft.com/).
    - Image files were formatted, resized and compressed using [Squoosh](https://squoosh.app/) image optimisation software.

### User Stories:

**User Story: View Home Page**

As a user,
I would like to view a homepage with a site description and purpose so that I can understand what Chaos Cards is and how to use it

Acceptance Criteria:
- The homepage must contain a site description, purpose, and navigation links.

Tasks:
- Create home.html
- Add static content
- Add navigation header and footer
- Test for accessibility

**User Story: Register for an Account**

As a user,
I would like to register for an account so that I can create, view, and manage my own cards

Acceptance Criteria:
- Registration form must validate inputs and create user accounts.

Tasks:
- Build Django registration view
- Add form validation
- Style form with crispy-forms
- Connect to user model
- Redirect on success

**User Story: Log In and Out**

As a user,
I would like to log in and log out so that I can securely access and manage my content

Acceptance Criteria:
- Login/logout links visible
- Conditional content rendered based on login state

Tasks:
- Implement Django login/logout
- Update header/footer to reflect auth status
- Test login flow

**User Story: Create Activity Card**

As a user,
I would like to create a new card with a title, description, and optional image so that I can save activities I want to do

Acceptance Criteria:
- Card form must allow title, description, and optional image upload

Tasks:
- Set up card model
- Create form with validation
- Integrate Cloudinary
- Build view and template

**User Story: Edit Activity Card**

As a user,
I would like to edit an existing card so that I can update my activity information

Acceptance Criteria:
- Edit page prepopulates card fields and saves changes on submit

Tasks:
- Create update view
- Reuse form
- Protect route via login
- Test for success messages

**User Story: Delete Activity Card**

As a user,
I would like to delete one of my cards so that I can remove outdated or unwanted activities

Acceptance Criteria:
- Delete option is only available to the card owner
- Confirmation is required

Tasks:
- Add delete view
- Protect via login
- Add confirmation modal or page

**User Story: View All My Cards**

As a user,
I would like to view all the cards I’ve created so that I can see my personal activity list

Acceptance Criteria:
- Only logged-in user’s cards are shown on their dashboard

Tasks:
- Filter cards by user
- Display in a list
- Add links to edit/delete

**User Story: Play the Chaos Card Game**

As a user,
I would like to press a "spin" button to get a random card so that I can choose a fun activity to do

Acceptance Criteria:
- Random card is shown after pressing spin
- Card shows title, description, and image

Tasks:
- Create "game" page
- Add JS or view logic to select a random card
- Style for UX

**User Story: See Login Status Across Pages**

As a user,
I would like to see whether I am logged in or not on every page so that I can know what actions I can take

Acceptance Criteria:
- Header reflects login state on all pages

Tasks:
- Add auth conditionals to base.html
- Style header with avatar/logout or login/register

**User Story: Admin Access**

As a superuser,
I would like to access the Django admin panel so that I can manage site content and users

Acceptance Criteria:
- Only superusers can access the admin route

Tasks:
- Enable admin in urls.py
- Register models
- Create superuser
- Test access

**User Story: Form Validation**

As a user,
I would like to receive clear error messages when submitting invalid forms so that I can easily fix mistakes

Acceptance Criteria:
- Form errors are displayed inline with helpful messages

Tasks:
- Use Django form validation
- Customize error messages
- Test common invalid inputs

**User Story: Notifications for Data Changes**

As a user,
I would like to receive confirmation when I create, edit, or delete a card so that I can know my actions were successful

Acceptance Criteria:
- Messages are shown after successful or failed actions

Tasks:
- Use Django messages framework
- Style alerts
- Display on relevant pages

### Wireframes:

The basic structure for Chaos Cards was worked out using the wireframe software [BALSAMIQ](https://balsamiq.com/), to guide design choices when developing. Over the project, the design changed and new sections were incorporated. Wireframes for desktop and mobile views were created.

**Desktop View**

![Desktop Wireframes](docs/design/desktop-wireframe.jpg)

**Mobile View**

![Mobile Wireframes](docs/design/wireframe-mobile.jpg)

### Database Design

An **Entity Relationship Diagram (ERD)** was planned and created to visualise the database, the different tables and their fields, and the relationships between tables before any development begun. The diagramming tool [Lucid Chart](https://www.lucidchart.com/) was used for this.

My project involved a simple database structure with 4 models:

- **User:**
    The user was related to the cards in a one-to-many relationship. The user was also related to about in a one-to-one relationship. Only the superuser can create an about section.
- **Card:**
    The card was related to the user in a many-to-one relationship.
- **About:**
    The about section was related to the user in a one-to-one relationship.
- **Contact / Feedback:**
    The contact / feedback model was unrelated to any of the other models. Anyone could use the contact form regardless of whether they are a registered user.

![ERD](docs/db/ERD-diagram.36.05.webp)

## Agile Working:

![Project Board](docs/design/project-board.png)

During development, I followed an agile, iterative mindset to deliver a usable MVP and continually refine the product. Key elements included:

- **Iterative testing and bug-fixing:** I regularly tested the application throughout development and addressed issues as they arose to maintain a stable baseline.
- **Scope adaptation:** Due to life distractions and illness in the initial weeks, I intentionally scoped back the project to its bare-bones must-haves for the MVP. This allowed steady progress while preserving the option to flesh out future features planned in the backlog.
- **Clear scope and intentions:** At the outset, I defined the project’s scope and objectives, created user stories that mapped to core functionality, and identified tasks to realize those stories.
- **Visual project management:** I set up a [project board](https://github.com/users/JamieJB123/projects/9) to track work using 'To Do', 'In Progress', and 'Done' columns, with a 'Backlog' column to store future features. This structure helped maintain organization, manage workflow, and monitor progress toward milestones.
- **Prioritization with MOSCOW:** I applied the MOSCOW method (Must-have, Should-have, Could-have, Won’t-have) to tag user stories. This prioritization supported disciplined scope management and ensured critical features were delivered first within the Kanban workflow.

**Outcome:**

The combination of iterative testing, disciplined scope management, and clear prioritization enabled a steady, transparent workflow focused on delivering a solid MVP while keeping room for future enhancements.

## Key Features:

- **User Authentication:**

    ![Registration / Log-in](docs/features/register-login.jpg)

    ![Registration](docs/features/register.jpg)

    ![Log-in](docs/features/log-in.jpg)

    ![Log-out](docs/features/logout.jpg)

    Registration, login/logout, password management via Django’s built-in auth system.
- **Card Management:**

    ![CRUD Functionality](docs/features/crud.jpg)

    Full CRUD functionality

    - Each registered user can create their own cards.

    - Each registered user can edit their own cards.

    - Each registered users can delete their own cards.

    - Users cannot see, edit or delete other users' cards.

    The superuser has full CRUD capabilities across users from the admin panel.
- **All Cards View:**

    Each user can see all of the cards which they have created.
- **Chaos Wheel:**

    ![Spin Functionality](docs/features/spin.jpg)

    Each registered user can play the *Chaos Cards* game.

    If a user is registered, they can 'spin the wheel of chaos', and a random card from the user's collection will be selected and displayed to them.

    If the user has not yet created their own cards and tries to play the game, an informative message will be displayed and they are directed towards the 'Create Cards' page so that they can play.

    ![No Cards](docs/features/nocards.jpg)

- **Contact Form:**

    ![Contact Form](docs/features/contact.jpg)

    Users can send feedback or queries, which is stored in the database and accessible in the admin panel.
- **Responsive Design:**

    Works seamlessly across devices and screen sizes.

## Deployment

**Hosting:** The project is deployed on [Heroku](https://www.heroku.com/) with a [PostgreSQL](https://www.postgresql.org/) database.

**Steps to Deploy:**
1. Create a new Heroku app
2. Initialise PostgreSQL database
3. Configure environment variables in Heroku Settings:
    - DATABASE_URL
    - SECRET_KEY
    - CLOUDINARY_URL
4. Virtual python environment created to install all dependencies for project.
5. Ensure DEBUG set to False when in production
6. Push code to GitHub and connect repo to Heroku
7. Deploy website manually from Heroku

**Security Considerations:**
- All sensitive keys stored in environment variables (and kept out of publically published code)
- Debug mode disabled in production
- Allowed hosts restricted to Heroku domain and custom domains

## AI Implementation:

### AI Usage and Implementation

AI was a valuable collaborator across idea generation, planning, development, and quality assurance — always used under careful human oversight.

**What AI contributed**

**User Story Generation**

Assisted in expanding and refining initial user stories.
Generated complementary variants to explore different user perspectives and workflows.

**Acceptance Criteria and Task Elaboration**

Helped articulate clear, testable acceptance criteria aligned with business goals.
Broke down high-level requirements into concrete tasks with logical sequencing and dependencies.

**ERD and Planning Support**

Useful for corroborating database design and entity relationships at the planning stage.

**Django Project Setup Guidance**

Served as a reference reminder for setup steps, project structure conventions, and recommended configuration order during initial scaffolding.

**Debugging Aid**

Provided hypothesis-generation and lightweight debugging guidance to explore potential root causes.
I used insights to drive targeted investigations rather than accepting AI-generated fixes wholesale, ensuring diagnosis remained human-led.

**Automated Testing Support**

Assisted in drafting test scenarios, edge-case coverage, and test data patterns.
Aided in outlining test hooks and fixtures, then validated the approach with manual review before implementation.

**Boilerplate and Semantic Guidance**

Offered boilerplate patterns for common tasks (e.g. views, forms, and tests) to accelerate setup while maintaining readability and consistency.
Recommended semantic and accessibility improvements, with final decisions and changes implemented by myself.

**Small, Supervised Code Generation**

Used for small, well-defined, low-risk tasks under direct supervision.
All generated code was reviewed, adapted, and integrated by me to ensure alignment with project standards and to avoid drift.

### Reflections:

**Human-in-the-loop**

AI outputs were considered as suggestions, not solutions. I critically evaluated relevance, context, and implications before adopting anything.

**Accessibility and Semantics**

Accessibility and semantic clarity were prioritized. AI suggestions were reviewed case-by-case and refined as needed.

**Outcome**

The project benefited from accelerated ideation, clarified acceptance criteria, and structured planning, while ensuring that higher-level thinking remained my work.

AI acted as a collaborative assistant and helped maintain focus on maintainability, accessibility, and correct architectural choices throughout development.

## Testing:

**Manual Testing:**

- Tested across Chrome, Firefox, Safari, and Edge
- Mobile responsiveness tested on multiple devices and simulated in DevTools
- Functional testing of all CRUD operations and wheel spin feature
- Tested that messages were displayed in response to user actions
- Tested form validation
- Tested that error handling and security handling (e.g. if tried to edit / delete other users' forms)

**Automated Testing:**

- Extensive unit testing was written to cover all views, forms and models in both the chaos_app app and about app.

- **Chaos App**
    - **Card Model**
        - Testing to cover basic card creation and validation
        - Testing string representation of models
        - Test field constraints (max-length)
        - Test default values (e.g. featured_image placeholder)
        - Tested model relationships (user foreign key with CASCADE delete)
        - Related name functionality
    - **Card Form**
        - Form validation with valid and invalid data
        - Field constraints (e.g. max-length)
        - Tested required fields (e.g. title, content)
        - Optional field handling
        - Form save functionality
    - **Views**
        - Authentication requirements (e.g. login_required decorator)
        - Valid and invalid data handling
        - User permission checks (e.g. can only edit/delete own cards)
        - Success and error message testing
        - Template rendering and redirects
        - Edge cases and error handling
        - Spin functionality
        - CRUD operations, pagination, GET/POST requests
- **About App:**
    - **Models:**
        - Model creation and validation
        - String representation
        - Field constraints (max-length, unique constraint)
        - Default values (e.g. image placeholder)
        - One-to-One field relationship
        - Cascade delete behaviour
    - **Forms:**
        - Form validation with valid and invalid data
        - Field constraints
        - Required field validation
        - Email format validation
        - Form save functionality
    - **Views:**
        - Basic view functionality and template rendering
        - Context data (about instance and form)
        - Valid and invalid form submissions
        - Form validation and error handling
        - Database record creation
        - Success and error messages
        - Redirect behaviour after submission


**Performance Testing:**

Lighthouse tests were run on each separate web page of the web application for performance, accessibility, best practice and SEO.

Initial lighthouse tests scored poorly on accessibility and best practices for the following reasons:

- Poor contrast between background and foreground
- Missing aria-labels
- Non-sequentially descending order of heading elements
- Cloudinary was returning images with insecure URLs (http://)

It was easy to resolve the first three issues through changing the colour scheme and styling, inserting aria-labels where needed, and ensuring the heading elements followed a sequentially descending order.

The Cloudinary issue was more difficult to resolve. Cloudinary was not automatically generating secure URL links for images which was causing performance and security issues.

I tried various solutions, such as adding the following code to my settings.py file:

![Cloudinary Security Fix Attempt](docs/testing/cloudinary-fix-attempt.png)

(*With my own cloud name, api key and api secret inserted*)

I also tried inserting security into the Django templates. However, none of this worked. In the end I resorted to hard coding https onto the front of the URLs in the templates and slicing the *http://* off. This has worked although it is a temporary solution.

### Lighthouse Test Results:

**Logged-in Home:**

![Lighthouse test for logged-in home page](docs/testing/logged-in-home-lighthouse.png)

**Logged-out Home:**

![Lighthouse test for logged-out home page](docs/testing/logout-lighthouse.png)

**About Page:**

![Lighthouse test for About page](docs/testing/about-lighthouse.png)

**My Cards Page:**

![Lighthouse test for 'My Cards' page](docs/testing/my-cards-lighthouse.png)

**Registration Page:**

![Lighthouse test for registration page](docs/testing/register-lighthouse.png)

**Log-in Page:**

![Lighthouse test for log-in page](docs/testing/logout-lighthouse.png)

**Log-out Page:**

![Lighthouse test for log-out page](docs/testing/logout-lighthouse.png)

### Code Validation:

**HTML Validation:**

I used the [W3C HTML Validator](https://validator.w3.org/) for code validation.

Results for all pages:
![HTML Validator Results](docs/testing/home-loggedin-html.png)

**CSS Validation:**

I used the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) for code validation.

Results:
![CSS Validator Results](docs/testing/Screenshot%202025-08-08%20at%2011.59.21.png)

**Python:**

Checked for PEP8 compliance with Flake8 and the [Code Institute Python Linter](https://pep8ci.herokuapp.com/).

**JavaScript:**

Used [JS Hint](https://jshint.com/) to validate JavaScript code (both JavaScript file in static folder and the small script inserted at the bottom of base.html). Alerted me to a few missing semi-colons.

## Future Enhancements:

- **Deck Management:** Organise cards into decks
- **Default themed decks** which users could 'spin'
- **Tagging:** Ability to tag your cards / decks with themes to enable users to search through public decks by theme
- **Favourites / starred:** Users could 'star' their favourite cards / decks which they find
- **Toggle Public / Private:** ability to choose public/private status for decks and cards
- **Ratings & Comments:** Let users rate and comment on public cards and decks
- **User Profiles & Stats:** User's would have their own personal profile page where they could see statistics about their website usage and interactions (e.g. number of spins, number of decks, comments, ratings etc.)
- **Public profiles:** user's could also have a public facing profile
- **Social Sharing:** Share chaos cards directly to social media
- **AI-Generated Cards:** Suggest chaos ideas based on user interests
- **Total Random Card:** User's could 'spin the wheel' from all public cards stored on the database

## Credits

- **Frameworks & Tools:** Django, Bootstrap, Cloudinary, Heroku, GitHub
- **Icons:** Font Awesome
- **Testing Resources:** W3C validators, Lighthouse, Flake8, JS Hint
- **Code Institute:** All the teachers, support and resources.
# chaos-cards-django-extent
