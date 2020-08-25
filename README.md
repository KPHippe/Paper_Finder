# Paper Finder


This project is designed to scrape ArXiv for the most recent articles,
find the most relevant articles based on keywords you search, and then email
you with the titles and links with downloads.


### Requirments

- beautifulsoup4=4.9.1
- requests=2.24.0

### Directions for setting up driver email

In order to have email functionality for this product, you need to set up your own gmail account/give access to python in your own gmail


#### Steps Once New GMail Created:
1. login to new account
2. Setup two-factor authentication, required for step 4
3. Visit [this link](https://myaccount.google.com/lesssecureapps?gar=1) to enable low security apps to access your account
4. In your account settings, go to Security>Signing Into Google>App Passwords
    - In 'select app' drop down, select 'custom' and in form give it a unique name
    - Copy password that is generated, this is the password that you will use in the configuration when setting sender password.

### TODO

- [x] ArXiv scraper
- [ ] BioarXiv scraper
- [X] email functionality
- [ ] cron job support
- [X] setup/install script
