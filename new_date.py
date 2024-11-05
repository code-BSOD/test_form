from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, FieldList, FormField
from wtforms.fields import DateField, StringField
from wtforms.validators import DataRequired, URL, NumberRange, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfnlasnflkadsnfal' 

class URLForm(FlaskForm):
    url = StringField('URL', validators=[URL(), DataRequired()])
    clicks = IntegerField('Clicks', validators=[DataRequired(), NumberRange(min=0)])
    impressions = IntegerField('Impressions', validators=[DataRequired(), NumberRange(min=0)])
    unique_clickthroughs = IntegerField('Unique Clickthroughs', validators=[Optional(), NumberRange(min=0)])
    unique_open = IntegerField('Unique Open', validators=[Optional(), NumberRange(min=0)])
    opens = IntegerField('Opens', validators=[Optional(), NumberRange(min=0)])

class MarketingForm(FlaskForm):
    date = StringField('Campaign Date', validators=[DataRequired()])  
    channel_type = SelectField('Channel Type', choices=[
        ('Landing Page', 'Landing Page'),
        ('Email', 'Email'), 
        ('Display/Banner', 'Banner'),
        ('Organic_Social', 'Organic_Social'),
        ('Package', 'Package'),
        ('Referral', 'Referral'),
        ('SEA', 'SEA'),
        ('Social_Media', 'Social_Media'),
        ('Technical Publication', 'Technical Publication'),
        ('Webinar', 'Webinar'),
    ])
    cost = DecimalField('Cost', places=2, validators=[DataRequired(), NumberRange(min=0)])
    region = SelectField('Region', choices=[('APAC', 'APAC'), ('Greater China', 'Greater China'), ('Global', 'Global'), ('Japan', 'Japan'), ('Americas', 'Americas')])
    campaign_name = StringField('Campaign Name', validators=[DataRequired()])
    purpose_of_activity = SelectField('Purpose of Activity', choices=[('Lead Generation', 'Lead Generation'), ('Awareness/Positioning', 'Awareness/Positioning')])
    description = StringField('Description', validators=[Optional()])
    registration = StringField('Registration', validators=[Optional()])
    comment = StringField('Comment', validators=[Optional()])
    added_by = StringField('Added By', validators=[DataRequired()])
    # date_added = StringField('Date Added', validators=[DataRequired()])  # This will now be a month input
    date_added = DateField('Date Added', format='%Y-%m-%d', validators=[DataRequired()])  # Revert back to DateField
    urls = FieldList(FormField(URLForm), min_entries=1)  # This will ensure at least one URL field is displayed
    delivered_emails = IntegerField('Delivered Emails', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MarketingForm()
    if form.validate_on_submit():
        # Process the form data here
        date = form.date.data  
        channel_type = form.channel_type.data
        cost = form.cost.data
        region = form.region.data
        campaign_name = form.campaign_name.data
        purpose_of_activity = form.purpose_of_activity.data
        description = form.description.data
        registration = form.registration.data
        comment = form.comment.data
        added_by = form.added_by.data
        date_added = form.date_added.data  
        urls = form.urls.data

        # Access delivered emails only if channel_type is Email
        delivered_emails = form.delivered_emails.data if channel_type == 'Email' else None

        # Print or process your data as needed
        print(f"Date: {date}, Region: {region}, Campaign Name: {campaign_name}, Purpose: {purpose_of_activity}, Description: {description}")
        print(f"Registration: {registration}, Comment: {comment}, Added By: {added_by}, Date Added: {date_added}")
        print(f"Delivered Emails: {delivered_emails}")
        
        for url_form in urls:  # Access URL and clicks for each link
            print(f"URL: {url_form.url.data}, Clicks: {url_form.clicks.data}, Impressions: {url_form.impressions.data}, Unique Clickthroughs: {url_form.unique_clickthroughs.data}, Unique Open: {url_form.unique_open.data}, Opens: {url_form.opens.data}")

        return 'Form submitted successfully!'
    return render_template('new_date.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
