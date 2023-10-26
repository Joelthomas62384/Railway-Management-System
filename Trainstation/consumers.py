from channels.generic.websocket import WebsocketConsumer
import json
from . models import *
from asgiref.sync import async_to_sync,sync_to_async
import datetime


class PlatformUpdate(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]['id']
        self.room_group_name = "platform_%s" % self.room_name
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        routes = Route.objects.get(route_id=self.room_name)
        train_tracking = Train_tracking.objects.filter(route=routes).get(date=datetime.datetime.today())
        route_stops = RoutesArrived.objects.filter(train_tracking=train_tracking)
        data = {}
        for i in route_stops:
            data[f"p{i.id}"] = i.Platform

        self.send(text_data=json.dumps({"payload":data}))
        
    
        

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data,):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'platform_status',
                "payload":text_data
            }
        ) 

    def platform_status(self,event):
        print(event)
        data = json.loads(event['value'])
        self.send(json.dumps({
            'payload':data
        }))



class ArrivalUpdate(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]['id']
        self.room_group_name = "arrival_%s" % self.room_name
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        routes = Route.objects.get(route_id = self.room_name)
        train_tracking = Train_tracking.objects.filter(route=routes).get(date=datetime.datetime.today())
        route_arrived = RoutesArrived.objects.filter(train_tracking=train_tracking)
        arrived_filter = route_arrived.filter(Arrived=True)
        

        # Convert QuerySets to lists of dictionaries
        route_arrived_list = list(route_arrived.values())
        length_route_arrived = len(route_arrived)
        current_station = RoutesArrived.objects.filter(train_tracking=train_tracking,Arrived=False).first()
        # current_station_list = list(current_station)

        data = {}
        data['route_arrived'] = route_arrived_list
        # data['arrived_filter'] = arrived_filter_list
        # data['departed_filter'] = departed_list
        data['length'] = length_route_arrived
        data['arrived_len'] = len(arrived_filter)
        try:
            data['current_station'] = current_station.route_stops.station.name
        except:
            data['current_station'] = "Journey Finished"

        self.send(json.dumps({"payload":data}))



    def receive(self, text_data,):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'arrival_status',
                "payload":text_data
            }
        ) 





    def disconnect(self, code):
        print("disconnect")



    def arrival_status(self,event):
        print(event)
        data = json.loads(event['value'])
        self.send(json.dumps({
            'payload':data
        }))