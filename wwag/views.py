from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required
from MySQLdb import IntegrityError
import hashlib
from datetime import datetime
