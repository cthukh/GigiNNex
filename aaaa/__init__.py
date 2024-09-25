from flask import Flask, render_template, flash, redirect
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()