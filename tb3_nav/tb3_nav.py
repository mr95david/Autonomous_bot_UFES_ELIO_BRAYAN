#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
import time
import random

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        # Inicialización del nodo con el nombre 'obstacle_avoidance'
        super().__init__('obstacle_avoidance')
        # Creador de publicador para enviar comandos de movimiento
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        # Suscriptor para recibir datos del sensor LIDAR
        self.subscription = self.create_subscription(LaserScan, 'scan', self.lidar_callback, 10)
        # Distancia segura para evitar obstáculos, en metros
        self.safe_distance = 0.7
        # Tiempo desde el último cambio de dirección
        self.last_change_time = time.time()
        # Intervalo para cambiar de dirección, en segundos
        self.change_interval = random.uniform(7, 20)

    def lidar_callback(self, msg):
        # Función de retrollamada para el procesamiento de los datos LIDAR
        current_time = time.time()
        if current_time - self.last_change_time > self.change_interval:
            # Hora de cambiar de dirección
            self.turn()
            self.last_change_time = current_time
            return

        # Creación de un mensaje Twist para control de movimiento
        twist = Twist()
        # Definición del cono de detección en grados
        cone_in_degree = 45
        # Cálculo del número de rangos a considerar en el LIDAR
        num_ranges = int((len(msg.ranges) / 360) * cone_in_degree) // 2
        important_ranges = []
        # Obtención de los rangos relevantes del sensor
        important_ranges.extend(msg.ranges[:num_ranges])
        important_ranges.extend(msg.ranges[-num_ranges:])
        # Distancia mínima detectada
        min_distance = min(important_ranges)

        if min_distance < self.safe_distance:
            # Obstáculo demasiado cerca, girar a la izquierda
            twist.linear.x = 0.0
            twist.angular.z = 0.2
        else:
            # El camino está despejado, moverse hacia adelante
            twist.linear.x = 0.2
            twist.angular.z = 0.0

        # Publicación del mensaje Twist
        self.publisher.publish(twist)

    def turn(self):
        # Método para girar el robot
        twist = Twist()
        # Duración del giro, ajustable según sea necesario
        turn_duration = random.uniform(2, 5)
        # Velocidad angular, ajustable según la capacidad del robot
        angular_velocity = 0.2

        # Elección aleatoria de giro a la izquierda o derecha
        twist.angular.z = angular_velocity if random.choice([True, False]) else -angular_velocity

        # Publicación del mensaje Twist y pausa por la duración del giro
        self.publisher.publish(twist)
        time.sleep(turn_duration)

        # Detener el giro
        twist.angular.z = 0.0
        self.publisher.publish(twist)

        # Establecer un nuevo intervalo aleatorio para el próximo cambio de dirección
        self.change_interval = random.uniform(7, 20)

def main(args=None):
    # Función principal para iniciar el nodo
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()