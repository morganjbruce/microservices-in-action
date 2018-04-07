from nameko.events import BROADCAST, EventDispatcher, event_handler
from nameko.rpc import rpc
from nameko.timer import timer


class EventPublisherService:
    name = "publisher_service"

    dispatch = EventDispatcher()

    @rpc
    def publish(self, event_type, payload):
        self.dispatch(event_type, payload)


class AnEventListenerService:
    name = "an_event_listener_service"

    @event_handler("publisher_service", "an_event")
    def consume_an_event(self, payload):
        print("service {} received:".format(self.name), payload)


class AnotherEventListenerService:
    name = "another_event_listener_service"

    @event_handler("publisher_service", "another_event")
    def consume_another_event(self, payload):
        print("service {} received:".format(self.name), payload)


class ListenBothEventsService:
    name = "listen_both_events_service"

    @event_handler("publisher_service", "an_event")
    def consume_an_event(self, payload):
        print("service {} received:".format(self.name), payload)

    @event_handler("publisher_service", "another_event")
    def consume_another_event(self, payload):
        print("service {} received:".format(self.name), payload)
