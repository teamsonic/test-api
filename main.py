#!usr/bin/env Python

import json
from storm.locals import *
import web

urls = (
    '/', 'Index',
    '/language', 'Language',
    '/api/getcollection', 'GetCollection',
    '/api/getone/([0-9]*)', 'GetOne',
)


def getStore():
    database = create_database("postgres://Josh:teamSONICSHADOWamy@127.0.0.1:5432/Josh")
    store = Store(database)
    return store


class Index:
    
    def GET(self):
        with open('templates/index.html') as f:
            return f.read()



class Language:
    
    def GET(self):
        languages = []
        for lang in web.ctx.environ['HTTP_ACCEPT_LANGUAGE'].split(','):
            lang = lang.split(';q=')
            if len(lang) == 1:
                lang.append('1.0')
            languages.append(lang)
        sorted_languages = sorted(languages, key=lambda lang: lang[1], reverse=True)
        for lang in sorted_languages:
            if lang[0].startswith('en') or lang[0] == 'fr-CA':
                ret_lang = lang[0]
                break
        else:
            ret_lang = 'en-US'
        return ret_lang



class GetCollection:
    
    def GET(self):
        """
        Get the entire collection of people from the database
        """
        store = getStore()
        people = store.find(Person)
        return json.dumps([{
            'id': person.id,
            'name': person.name,
            'age': person.age,
        } for person in people])



class GetOne:


    def GET(self, person_id):
        """
        Get a single person from the database
        """
        if not person_id:
            raise Exception
        store = getStore()
        person = store.get(Person, int(person_id))
        return json.dumps({
            'id': person.id,
            'name': person.name,
            'age': person.age,
        }) 

    
    def POST(self, person_id):
        """
        Update a single person from the database
        """
        if not person_id:
            raise Exception
        data = json.loads(web.data())
        store = getStore()
        person = store.get(Person, int(person_id))
        for k, v in data.iteritems():
            if k == 'id':
                continue
            try:
                setattr(person, k, v)
            except TypeError:
                setattr(person, k, int(v))
        store.commit()
        return


    def PUT(self, person_id):
        """
        Add a new person to the database
        """
        if not person_id:
            store = getStore()
            person = store.add(Person())
            store.commit()
            return person.id


    def DELETE(self, person_id):
        """
        Delete a person from the database
        """
        if not person_id:
            raise Exception
        store = getStore()
        person = store.get(Person, int(person_id))
        store.remove(person)
        store.commit()


class Person(Storm):
    """
    I am a person
    """
    __storm_table__ = "person"
    id = Int(primary=True)
    name = Unicode()
    age = Int()
    


app = web.application(urls, locals())

if __name__ == '__main__':
    app.run()
