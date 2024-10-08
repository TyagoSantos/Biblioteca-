import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from app import atualizar_usuario


def test_atualizar_usuario_sucesso():
    user_id = 1
    nome = "Carlos Silva"
    email = "carlos.silva@example.com"
    telefone = "(11) 91234-5678"
    
    with patch("app.connect_db") as mock_connect_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        
        result = atualizar_usuario(user_id, nome, email, telefone)
        
        assert result["success"] is True
        assert result["message"] == "Usuário atualizado com sucesso"


def test_atualizar_usuario_sem_informacao():
    user_id = 1
    
    result = atualizar_usuario(user_id)
    
    assert result["success"] is False
    assert result["message"] == "Nenhuma informação para atualizar"


def test_atualizar_usuario_email_invalido():
    user_id = 1
    email = "carlos.silvaexample.com"  
    
    result = atualizar_usuario(user_id, email=email)
    
    assert result["success"] is False
    assert result["message"] == "E-mail inválido"


def test_atualizar_usuario_erro_bd():
    user_id = 1
    nome = "Carlos Silva"
    
    with patch("app.connect_db") as mock_connect_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.Error("Erro de banco de dados")
        
        result = atualizar_usuario(user_id, nome=nome)
        
        assert result["success"] is False
        assert result["message"] == "Erro de banco de dados"


