"""
Servicio de Kafka Producer para envío de logs y mensajes
"""
import json
import logging
from typing import Optional, Dict
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from src.config.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_CLIENT_ID,
    KAFKA_REQUEST_TOPIC,
    KAFKA_REQUEST_TIMEOUT,
    KAFKA_CONNECTION_TIMEOUT,
    KAFKA_ENABLED
)


class KafkaProducerService:
    """
    Servicio para producir mensajes a Kafka con manejo de errores y conexión opcional
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.producer: Optional[KafkaProducer] = None
        self.is_connected = False
        self.request_log_topic = KAFKA_REQUEST_TOPIC
        
    async def initialize(self):
        """
        Inicializa la conexión con Kafka
        Si falla, el servidor continuará funcionando sin Kafka
        """
        if not KAFKA_ENABLED:
            self.logger.info("Kafka está deshabilitado en la configuración")
            return
            
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                client_id=KAFKA_CLIENT_ID,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=5,
                request_timeout_ms=KAFKA_REQUEST_TIMEOUT,
                api_version=(0, 10, 1)
            )
            
            # Test de conexión con timeout
            self.producer.bootstrap_connected()
            
            self.is_connected = True
            self.logger.info("Kafka Producer conectado exitosamente")
            
        except Exception as error:
            self.is_connected = False
            self.logger.warning(
                f"Kafka no disponible - El servidor funcionará sin Kafka (solo logs a archivo): {str(error)}"
            )
    
    def produce_async(self, topic: str, message: dict, headers: Optional[Dict[str, str]] = None) -> bool:
        """
        Envía un mensaje a Kafka de forma asíncrona
        
        Args:
            topic (str): Topic de Kafka
            message (dict): Mensaje a enviar
            headers (dict, optional): Headers del mensaje
            
        Returns:
            bool: True si se envió exitosamente, False si falló o Kafka no está disponible
        """
        if not self.is_connected:
            return False
            
        try:
            # Convertir headers a formato Kafka
            kafka_headers = []
            if headers:
                kafka_headers = [(k, v.encode('utf-8')) for k, v in headers.items()]
            
            # Enviar mensaje
            future = self.producer.send(
                topic,
                value=message,
                headers=kafka_headers if kafka_headers else None
            )
            
            # Obtener metadata del envío
            record_metadata = future.get(timeout=10)
            
            self.logger.info(
                f"Mensaje entregado a {topic} [{record_metadata.partition}] "
                f"con Offset: {record_metadata.offset}"
            )
            return True
            
        except KafkaTimeoutError:
            self.logger.error("Timeout al enviar mensaje a Kafka")
            return False
        except KafkaError as error:
            self.logger.error(f"Error al enviar mensaje a Kafka: {str(error)}")
            return False
        except Exception as error:
            self.logger.error(f"Error inesperado al enviar mensaje a Kafka: {str(error)}")
            return False
    
    def produce_request_log_async(self, message: dict, headers: Optional[Dict[str, str]] = None) -> bool:
        """
        Envía un log de request al topic configurado
        
        Args:
            message (dict): Log del request
            headers (dict, optional): Headers del mensaje
            
        Returns:
            bool: True si se envió exitosamente
        """
        return self.produce_async(self.request_log_topic, message, headers)
    
    def disconnect(self):
        """
        Cierra la conexión con Kafka
        """
        if self.producer and self.is_connected:
            try:
                self.producer.flush()
                self.producer.close()
                self.is_connected = False
                self.logger.info("Kafka Producer desconectado")
            except Exception as error:
                self.logger.error(f"Error al desconectar Kafka Producer: {str(error)}")


# Singleton del servicio
kafka_producer_service = KafkaProducerService()
