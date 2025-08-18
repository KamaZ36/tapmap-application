from enum import Enum


class OrderStatus(str, Enum): 
    driver_search = 'driver_search'
    waiting_driver = 'waiting_driver'
    driver_waiting_customer = 'driver_waiting_customer'
    processing = 'processing'
    completed = 'completed'
    cancelled = 'cancelled'
    