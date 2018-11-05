#User/Page Flow
- volunteer: not eligble
Home.html -> volunteer.html -> NotEligibleVolunteer.html
- volunteer: eligible
Home.html -> volunteer.html -> EligibleVolunteer.html -> ShiftSignUpPage (html TBD) -> VolunteerConfirmation -> ScheduleViewer.html
- organization
Home.html -> organizer.html -> OrganizationConfirmation.html -> ScheduleViewer.html 
- About Us.html: linked from header on all pages
- Contact Us.html : linked from header on all pages

#To- do list
- &  not started
- ^  in progress by YY(your initials)
- *  completed

#General
- ^by MC Heroku deployment
- & Learning.MD, to do for everyone
- & Rehearse for presentation, 1pm on Friday 12/8

#Must Have
- ^by LS  consistent styling across all pages

Volunteer Verification
- ^by YY  parse API response, route to appropriate html page
- ^by YY  pasrse API response, return the applicable shifts for volunteer
- & Remove name and license field on volunteer.html
- & Add "powered by BetterDoctor" and BetterDoctor logo on volunteer.html, see https://developer.betterdoctor.com/display-requirements

Shift Sign Up
- & Shift Sign Up Page html, display applicable shift for volunteer (filterd by specialty etc), button for each shift
- ^by YY  create volunteer table 
- & Associate volunteer ID with shift upon shift sign up

Confirmation
- & Add link on VolunteerConfirmation.html to ScheduleViewer.html
- & Add link on OrganizationConfirmation.html to ScheduleViewer.html
- & Add link on OrganizationConfirmation.html to "Schedule another shift", direct back to Organizer.html

Organization Page
- & Add quantity field in organizer.html
- & Add calendar selector, limit selection to 14 days
- ^by YY get info from form to create shifts in table

Schedule (scheduleViewer.html is shared by volunteer and organizer)
- & Display all shifts 
- & Filter shifts by NPI

#Nice to Have
- & power contact form with mailgun API (I think if this is too complicated with the deployment, we can just link to an email address with mailto instead)
- & Google calendar "Add to calendar integration"
- & Javascript form validation
- & extra credit: build and consume another API





