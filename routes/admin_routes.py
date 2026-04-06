from flask import Blueprint, render_template, request, redirect, url_for
from models.admin_model import *

admin_bp = Blueprint('admin', __name__)