from channels.generic.websocket import WebsocketConsumer
import json
from . models import *
from asgiref.sync import async_to_sync,sync_to_async
import datetime


class PaymentUpdate(WebsocketConsumer):
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

