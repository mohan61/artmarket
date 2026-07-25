from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class ArtistRegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    bio = TextAreaField("Short bio / artist statement", validators=[Optional(), Length(max=2000)])


class CustomerRegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    address = StringField("Default shipping address", validators=[Optional(), Length(max=255)])


class ArtworkForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    price = DecimalField("Price (USD)", validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField(
        "Category",
        choices=[
            ("Painting", "Painting"),
            ("Photography", "Photography"),
            ("Sculpture", "Sculpture"),
            ("Digital Art", "Digital Art"),
            ("Illustration", "Illustration"),
            ("Mixed Media", "Mixed Media"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )
    image = FileField(
        "Artwork image",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only!")],
    )


class OrderForm(FlaskForm):
    quantity = IntegerField("Quantity", default=1, validators=[DataRequired(), NumberRange(min=1, max=10)])
    shipping_address = TextAreaField("Shipping address", validators=[DataRequired(), Length(max=255)])
