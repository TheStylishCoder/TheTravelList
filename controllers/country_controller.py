from flask import Flask, render_template, request, redirect
from flask import Blueprint 

from models.country import Country
import repositories.country_repository as country_repository

countries_blueprint = Blueprint("countries", __name__)

@countries_blueprint.route("/countries")
def countries():
    countries = country_repository.select_all()
    return render_template("countries/index.html", countries = countries)

@countries_blueprint.route("/countries/<id>", methods=['GET'])
def show(id):
    country = country_repository.select(id)
    cities = country_repository.cities(country)
    return render_template("countries/show.html", country = country, cities = cities)

@countries_blueprint.route("/countries/<id>/edit", methods=['GET'])
def edit_country(id):
    country = country_repository.select(id)
    return render_template("countries/edit.html", country = country)

@countries_blueprint.route("/countries/<id>", methods=['POST'])
def update_country(id):
    name = request.form['name']
    visited = request.form['visited']
    wishlist = request.form['wishlist']
    country = Country(name, visited, wishlist, id)
    country_repository.update(country)
    return redirect('/countries')

@countries_blueprint.route("/countries/new", methods=['GET'])
def new_country():
    return render_template("countries/new.html")

@countries_blueprint.route("/countries", methods=['POST'])
def create_country():
    name = request.form['name']
    visited = request.form['visited']
    wishlist = request.form['wishlist']
    country = Country(name, visited, wishlist)
    country_repository.save(country)
    return redirect("/countries")

@countries_blueprint.route("/countries/<id>/delete", methods=['POST'])
def delete_country(id):
    country_repository.delete(id)
    return redirect('/countries')

@countries_blueprint.route("/countries/search", methods=['GET'])
def search_for_country():
    return render_template("countries/search.html")

@countries_blueprint.route("/countries/search_results", methods=['POST'])
def search_results():
    search = request.form['search']
    countries = country_repository.search(search)
    return render_template("results.html", countries = countries)