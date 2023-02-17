from neomodel import (config, StructuredNode, StructuredRel, RelationshipTo)
from neomodel import StringProperty, IntegerProperty, ArrayProperty, UniqueIdProperty

config.DATABASE_URL = 'bolt://neo4j:password@127.0.0.1:7688'

class About(StructuredRel): pass
class Actor(StructuredRel): pass
class Affiliation(StructuredRel): pass
class AlumniOf(StructuredRel): pass
class Award(StructuredRel): pass
class Author(StructuredRel): pass
class BirthPlace(StructuredRel): pass
class Brand(StructuredRel): pass
class ByArtist(StructuredRel): pass
class Character(StructuredRel): pass
class Children(StructuredRel): pass
class ConnectedTo(StructuredRel): pass
class ContainedInPlace(StructuredRel): pass
class ContainsPlace(StructuredRel): pass
class Colorist(StructuredRel): pass
class Competitor(StructuredRel): pass
class Composer(StructuredRel): pass
class ContentLocation(StructuredRel): pass
class Director(StructuredRel): pass
class DeathPlace(StructuredRel): pass
class Depth(StructuredRel): pass
class Editor(StructuredRel): pass
class Gender(StructuredRel): pass
class HomeLocation(StructuredRel): pass
class HasPart(StructuredRel): pass
class Height(StructuredRel): pass
class Location(StructuredRel): pass
class InLanguage(StructuredRel): pass
class IsBasedOn(StructuredRel): pass
class Organizer(StructuredRel): pass
class Parent(StructuredRel): pass
class Width(StructuredRel): pass
class Creator(StructuredRel): pass
class FamilyName(StructuredRel): pass
class Founder(StructuredRel): pass
class GivenName(StructuredRel): pass
class Producer(StructuredRel): pass
class Provider(StructuredRel): pass
class Publisher(StructuredRel): pass
class Sponsor(StructuredRel): pass
class Sport(StructuredRel): pass
class Translator(StructuredRel): pass
class WorksFor(StructuredRel): pass
class Weight(StructuredRel): pass
class NetWorth(StructuredRel): pass

class Resource(StructuredNode):
    uri = StringProperty(unique_index=True, required=True)
    label = StringProperty(db_property="rdfs__label")
    alternateName = StringProperty(db_property="sch__alternateName")
    birthDate = StringProperty(db_property="sch__birthDate")
    
    about = RelationshipTo("Resource", 'sch__about', model=About)
    actor = RelationshipTo("Resource", 'sch__actor', model=Actor)
    affiliation = RelationshipTo("Resource", 'sch__affiliation', model=Affiliation)
    alumniOf = RelationshipTo("Resource", 'sch__alumniOf', model=AlumniOf)
    award = RelationshipTo("Resource", 'sch__award', model=Award)
    author = RelationshipTo("Resource", 'sch__author', model=Author)
    birthPlace = RelationshipTo("Resource", 'sch__birthPlace', model=BirthPlace)
    brand = RelationshipTo("Resource", 'sch__brand', model=Brand)
    byArtist = RelationshipTo("Resource", 'sch__byArtist', model=ByArtist)
    character = RelationshipTo("Resource", 'sch__character', model=Character)
    children = RelationshipTo("Resource", 'sch__children', model=Children)
    colorist = RelationshipTo("Resource", 'sch__colorist', model=Colorist)
    competitor = RelationshipTo("Resource", 'sch__competitor', model=Competitor)
    composer = RelationshipTo("Resource", 'sch__composer', model=Composer)
    connectedTo = RelationshipTo("Resource", 'sch__connectedTo', model=ConnectedTo)
    containedInPlace = RelationshipTo("Resource", 'sch__containedInPlace', model=ContainedInPlace)
    containsPlace = RelationshipTo("Resource", 'sch__containsPlace', model=ContainsPlace)
    contentLocation = RelationshipTo("Resource", 'sch__contentLocation', model=ContentLocation)
    creator = RelationshipTo("Resource", "sch__creator", model=Creator)
    director = RelationshipTo("Resource", "sch__director", model=Director)
    deathPlace = RelationshipTo("Resource", 'sch__deathPlace', model=DeathPlace)
    depth = RelationshipTo("Resource", 'sch__depth', model=Depth)
    editor = RelationshipTo("Resource", "sch__editor", model=Editor)
    familyName = RelationshipTo("Resource", 'sch__familyName', model=FamilyName)
    founder = RelationshipTo("Resource", 'sch__founder', model=Founder)
    givenName = RelationshipTo("Resource", 'sch__givenName', model=GivenName)
    gender = RelationshipTo("Resource", 'sch__gender', model=Gender)
    homeLocation = RelationshipTo("Resource", 'sch__homeLocation', model=HomeLocation)
    hasPart = RelationshipTo("Resource", 'sch__hasPart', model=HasPart)
    height = RelationshipTo("Resource", 'sch__height', model=Height)
    inLanguage = RelationshipTo("Resource", 'sch__inLanguage', model=InLanguage)
    isBasedOn = RelationshipTo("Resource", 'sch__isBasedOn', model=IsBasedOn)
    location = RelationshipTo("Resource", 'sch__location', model=Location)
    organizer = RelationshipTo("Resource", 'sch__organizer', model=Organizer)
    parent = RelationshipTo("Resource", "sch__parent", model=Parent)
    producer = RelationshipTo("Resource", "sch__producer", model=Producer)
    provider = RelationshipTo("Resource", "sch__provider", model=Provider)
    publisher = RelationshipTo("Resource", "sch__publisher", model=Publisher)
    sponsor = RelationshipTo("Resource", "sch__sponsor", model=Sponsor)
    sport = RelationshipTo("Resource", "sch__sport", model=Sport)
    translator = RelationshipTo("Resource", "sch__translator", model=Translator)
    worksFor = RelationshipTo("Resource", "sch__worksFor", model=WorksFor)
    weight = RelationshipTo("Resource", "sch__weight", model=Weight)
    
    netWorth = RelationshipTo("sch__QuantitativeValue", 'sch__netWorth', model=NetWorth)

class sch__GeoCoordinates(Resource):
    # uri = StringProperty(unique_index=True, required=True)
    latitude = StringProperty(db_property="sch__latitude")
    longitude = StringProperty(db_property="sch__longitude")

class sch__QuantitativeValue(Resource):
    # uri = StringProperty(unique_index=True, required=True)
    maxValue = StringProperty(db_property="sch__maxValue")
    minValue = StringProperty(db_property="sch__minValue")
    value = StringProperty(db_property="sch__value")

