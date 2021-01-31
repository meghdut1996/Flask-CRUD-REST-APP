from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

##initialize the app
app=Flask(__name__)

#configuration
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///mydb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

###initialize the db
db = SQLAlchemy(app)

##### create event model class
class Event(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(50))
    Decription=db.Column(db.String(200))
    Datefrom=db.Column(db.DateTime)
    Dateto=db.Column(db.DateTime)
    Location=db.Column(db.String(200))
    Imgurl=db.Column(db.String(200))
    Status=db.Column(db.String(20))
    
#####create memeber model class
class Member(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    Firstname=db.Column(db.String(50))
    Lastname=db.Column(db.String(50))
    Churchname=db.Column(db.String(200))
    Gender=db.Column(db.String(20))
    ContactInfo=db.Column(db.String(50))
    
###create event_member model class
class Event_Member(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    Event_id=db.Column(db.Integer)
    Member_id=db.Column(db.Integer)
    Status=db.Column(db.String(50))

###index route
@app.route("/")
def index():
    return jsonify({'message': 'Hello!, this is a test ouput it means that your app ai running'})


####create event
@app.route("/event/",methods=['POST'])
def create_event():
    event_data=request.get_json()
    if event_data:
        datefrom=event_data['Datefrom']
        dateto=event_data['Dateto']
        ##transform the json data inputs to an object which python can understand
        datefrom_object=datetime.strptime(datefrom, '%Y-%m-%d %H:%M:%S') #strptime is used to convert a date string to a datetime object.
        dateto_object=datetime.strptime(dateto, '%Y-%m-%d %H:%M:%S')
        ##create new event
        new_event=Event(
            Name=event_data['Name'],
            Decription=event_data['Decription'],
            Datefrom=datefrom_object,
            Dateto=dateto_object,
            Location=event_data['Location'],
            Imgurl=event_data['Imgurl'],
            Status=event_data['Status']
            )
        ##save to db
        db.session.add(new_event)
        db.session.commit()          
        ###create a response that the change successfull
        return jsonify({'message': 'New event has been created'})     
    else:
        return jsonify({'error': 'No Data passed'})


### read all event
@app.route('/event/',methods=['GET'])
def read_all_event():
    all_events=Event.query.all()
    if all_events:
        #create blank list
        all_events_output=[]
        for event in all_events:
            ##build indiviual record
            each_event={}
            each_event['id']=event.id
            each_event['Name']=event.Name
            each_event['Decription']=event.Decription
            each_event['Datefrom']=event.Datefrom
            each_event['Dateto']=event.Dateto
            each_event['Location']=event.Location
            each_event['Imgurl']=event.Imgurl
            each_event['Status']=event.Status
            #build output list
            all_events_output.append(each_event)
        return jsonify({'message': all_events_output})   
    else:
        return jsonify({'error':'No event passed'})

### read one event
@app.route("/event/<id>/",methods=['GET'])
def read_one_event(id):
    one_event=Event.query.filter_by(id=id).first()
    if one_event:
        event={}
        event['id']=one_event.id
        event['Name']=one_event.Name
        event['Decription']=one_event.Decription
        event['Datefrom']=one_event.Datefrom.strftime('%Y-%m-%d %H:%M:%S') #strftime() is used to convert a time to string.
        event['Dateto']=one_event.Dateto.strftime('%Y-%m-%d %H:%M:%S')
        event['Location']=one_event.Location
        event['Imgurl']=one_event.Imgurl
        event['Status']=one_event.Status
        return jsonify({'event':event})
    else:
        return jsonify({'error':'No event found'}) 
    
## UPDATE EXISTING RESOURCES
@app.route('/event/<id>/',methods=['PUT'])
def update_event(id):
    #check if there is data passed
    event_data=request.get_json()
    if event_data:
        ##check if record exist
        update_event=Event.query.filter_by(id=id).first()
        if update_event:
            update_event.Name=event_data['Name']
            update_event.Decription=event_data['Decription']
            update_event.Datefrom=datetime.strptime(event_data['Datefrom'], '%Y-%m-%d %H:%M:%S')
            update_event.Dateto=datetime.strptime(event_data['Dateto'], '%Y-%m-%d %H:%M:%S')
            update_event.Location=event_data['Location']
            update_event.Status=event_data['Status']
            #save to db
            db.session.commit()
            ## throw success message
            return jsonify({'message': 'Event has been updated'})  
        else:
            return jsonify({'error': 'No event found'})
    else:
        return jsonify({'error': 'No Data passed'})
        

### delete event
@app.route("/event/<id>/",methods=['DELETE'])
def delete_one_event(id):
    delete_event=Event.query.filter_by(id=id).first()
    if delete_event:
        db.session.delete(delete_event)
        db.session.commit()
        return jsonify({'message':'Event has been deleted'})
    else:
        return jsonify({'error':'No event found!'})

    
    
### create member
@app.route("/member/",methods=['POST'])
def create_memeber():
    member=request.get_json()
    if member:
        new_member=Member(
            Firstname=member['Firstname'],
            Lastname=member['Lastname'],
            Churchname=member['Churchname'],
            Gender=member['Gender'],
            ContactInfo=member['ContactInfo']
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message':'Member has been created'})
    else:
        return jsonify({"error":"No Data passed"})

    
##### show all the member value
@app.route("/member/",methods=['GET'])
def all_members():
    all_member=Member.query.all()
    if all_member:
        all_member_output=[]
        for i in all_member:
            each_member={}
            each_member['id']=i.id
            each_member['Firstname']=i.Firstname
            each_member['Lastname']=i.Lastname
            each_member['Churchname']=i.Churchname
            each_member['Gender']=i.Gender
            each_member['ContactInfo']=i.ContactInfo
            all_member_output.append(each_member)
        return jsonify({'message': all_member_output})
    else:
        return jsonify({'error':'No Member found'})
    
    
### read on member
@app.route("/member/<id>/",methods=['GET'])
def read_one_member(id):
    one_member=Member.query.filter_by(id=id).first()
    if one_member:
        member={}
        member['id']=one_member.id
        member['Firstname']=one_member.Firstname
        member['Lastname']=one_member.Lastname
        member['Churchname']=one_member.Churchname
        member['Gender']=one_member.Gender
        member['ContactInfo']=one_member.ContactInfo
        return jsonify({'member':member})     
    else:
        return jsonify({'error': 'No Member found'})


### update one member
@app.route("/member/<id>/",methods=['PUT'])
def update_member(id):
    member_data=request.get_json()
    if member_data:
        exist_member=Member.query.filter_by(id=id).first()
        if exist_member:
            exist_member.Firstname=member_data['Firstname']
            exist_member.Lastname=member_data['Lastname']
            exist_member.Churchname=member_data['Churchname']
            exist_member.Gender=member_data['Gender']
            exist_member.ContactInfo=member_data['ContactInfo']
            db.session.commit()
            return jsonify({'message':'Member has been updated'})
        else:
            return jsonify({'error':'No Member found'})
    else:
        return jsonify({'error':'No Data passed'})
    
#delete member
@app.route("/member/<id>/", methods=['DELETE'])
def delete_member(id):
    exist_member=Member.query.filter_by(id=id).first()
    if exist_member:
        db.session.delete(exist_member)
        db.session.commit()
        return jsonify({'message':'Member has been deleted'})
    else:
        return jsonify({'error':'No Member found'})


### create event_member
@app.route("/event_member/",methods=['POST'])
def create_event_member():
    event_member_data=request.get_json()
    if event_member_data:
        event=Event.query.filter_by(id=int(event_member_data['Event_id'])).first()
        if event:
            member=Member.query.filter_by(id=int(event_member_data['Member_id'])).first()
            if member:
                event_member_exist=Event_Member.query.filter(
                    Event_Member.Event_id==int(event_member_data['Event_id']),
                    Event_Member.Member_id==int(event_member_data['Member_id'])).first()
                if event_member_exist:
                    return jsonify({'error':'event already exist'})
                else:
                    #create instance
                    new_event_member=Event_Member(
                        Event_id=int(event_member_data['Event_id']),
                        Member_id=int(event_member_data['Member_id']),
                        Status=event_member_data['Status']
                    )
                    # commit db
                    db.session.add(new_event_member)
                    db.session.commit()
                    # throw a message
                    return jsonify({'message':'Event Member has been created successfully'})
            else:
                return jsonify({'error':'No member found'})
        else:
            return jsonify({'message':'No Event found'})
    else:
        return jsonify({'error':'No event found'})

    
## read all event_member records based on given event_id
@app.route("/event_member_by_eventid/<Event_id>/",methods=['GET'])
def read_event_member(Event_id):
    all_event_member=Event_Member.query.filter_by(Event_id=Event_id).all()
    if all_event_member:
        event_member_ouput=[]
        for i in all_event_member:
            each_event={}
            each_event['id']=i.id
            each_event['Event_id']=i.Event_id
            each_event['Member_id']=i.Member_id
            event_member_ouput.append(each_event)
        return jsonify({'message':event_member_ouput})       
    else:
        return jsonify({'error':'No Event Member Found'})


## read all event_member records based on given member_id
@app.route("/event_member_by_memberid/<Member_id>/",methods=['GET'])
def read_all_event_member_by_memberid(Member_id):
    all_event_members=Event_Member.query.filter_by(Member_id=Member_id).all()
    if all_event_members:
        event_member_ouput=[]
        for i in all_event_members:
            each_event={}
            each_event['id']=i.id
            each_event['Event_id']=i.Event_id
            each_event['Member_id']=i.Member_id
            event_member_ouput.append(each_event)
        return jsonify({'message':event_member_ouput})
    else:
        return jsonify({"error":"No Event Member passed"})
    
## update event memeber
@app.route("/event_member_by_memberid/<event_id>/",methods=['PUT'])
def update_event_member(event_id):
    event_member_data=request.get_json()
    if event_member_data:
        update_event_member=Event_Member.query.filter_by(id=id).first()
        if update_event_member:
            ###update the instance
            update_event_member.Status=event_member_data['Status']
            ###save to db
            db.session.commit()
            return jsonify({'message':'Event Member successfuly updated'})
        else:
            return jsonify({'error':'No Event Member Found'})
    else:
        return ({'error':'No Data Passed'})
    
### delete event_member
@app.route("/event_memeber/<id>/",methods=['DELETE'])
def delete_event_member(id):
    delete_event_member=Event_Member.query.filter_by(id=id).first()
    if delete_event_member:
        db.session.delete(delete_event_member)
        db.session.commit()
        return jsonify({'message':"Event Member has been deleted successfull"})
    else:
        return jsonify({"error":"No event found"})

#run the app
if __name__=="__main__":
    app.run(debug=True)