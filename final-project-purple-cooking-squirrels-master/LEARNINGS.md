#URL:https://good-neighbor-i253-1.herokuapp.com/index

#Good Neighbor - Background

A platform connecting volunteers to aid organizations in disaster relief efforts.
Natural disasters, armed conflicts, and other catastrophic events have a huge impact on local communities and threaten the lives and well beings of those affected
			
Good Neighbor aims to empower disaster recovery by connecting skilled volunteers with larger organizations leading disaster relief efforts. By putting people with the right skills at the right place and time, we hope to make the society more resilient in the face of pressure and catastrophe

Whether you are a volunteer with experience in healthcare or disaster response or are a part of a larger organization faced with challenges and in need of people, Good Neighbor hopes to aid you in your action and effort

Our project is a web application which acts as an interface between volunteers and relief organizations. The platform consists of two avenues, one for disaster relief organizers and one for volunteers who would like to serve.

#Good Neighbor - Functionalities
General
- About us - the story behind Good Neighbor
- Contact - contact form that allows people to send messages and questions to the Good Neighbor team

For Relief Organizations
- Ability to request volunteers by specifying the type of skills needed and the number of volunteers needed for each day
- Ability to view a schedule for all of the volunteer shifts
- Ability to see only the unfilled shifts that still need volunteers
- Ability to see shifts by skills needed/specialty
- Ability to see volunteers that have signed up for shifts (all volunteers are verified healthcare professionals!)

For Volunteers
- Ability to get license verification by entering only the NPI 
- Ability to view shifts based on the volunteer's specialty
- Ability to sign up for shifts
- Ability to view schedules with shift and other volunteers for the shift


#Web Technologies used
1. HTML: Provides the content/barebones for the website
2. CSS: Provides the styling for the HTML content
3. JS: Allows interactivity
4. Bootstrap: Used bootstrap framework for main styling (in conjunction with custom styling in the HTML style portion)
5. SQLite: Used in our application as the database, where we store data relating to the shifts created by organizations and information of volunteers who sign up
6. Flask: Used flask as a framework to use extensions like render template and request
7. Python:Used python to program the webserver, where the logic and flow of the application is
8. JSON: Received data in JSON format from BetterDoctor API
9. BetterDoctor API: Retrieved data about doctor's specialty and license
10. Mailgun API:used mailgun API to power the contact form
