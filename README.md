# Lungscan

Esta API fornece serviços de análise de imagens de raio-X pulmonar utilizando modelos de inteligência artificial para detectar patologias.

## Endpoints da API

### Informações Gerais
```
GET /
```
Retorna informações básicas sobre a API.

**Resposta**:
```json
{
    "message": "Lung Scan API",
    "version": "1.0.0",
    "endpoints": {
        "analyze": "/api/v1/analyze",
        "pathologies": "/api/v1/pathologies",
        "health": "/api/v1/health",
        "random_image": "/api/v1/random-image"
    }
}
```

### Verificação de Saúde
```
GET /api/v1/health
```
Verifica o status de saúde da API.

**Resposta**:
```json
{
    "status": "healthy",
    "timestamp": "2024-03-21T10:00:00Z"
}
```

### Listar Patologias Suportadas
```
GET /api/v1/pathologies
```
Retorna a lista de patologias que o modelo pode detectar.

**Resposta**:
```json
{
    "pathologies": [
        "pneumonia",
        "covid19",
        "tuberculose",
        // ... outras patologias
    ]
}
```

### Analisar Imagem
```
POST /api/v1/analyze
```
Analisa uma imagem de raio-X pulmonar e retorna as patologias detectadas.

**Requisição**:
- Content-Type: `multipart/form-data`
- Corpo: arquivo de imagem (formato: jpg, png)
- Tamanho máximo do arquivo: 16MB

**Resposta**:
```json
{
    "predictions": {
        "pneumonia": 0.95,
        "covid19": 0.12,
        "normal": 0.03
    },
    "processing_time": "1.2s",
    "model_version": "densenet121-res224-all"
}
```

### Gerar Imagem de Teste
```
GET /api/v1/random-image
```
Gera uma imagem de teste aleatória para fins de desenvolvimento.

**Resposta**:
- Content-Type: `image/png`
- Corpo: arquivo de imagem

## Limites e Restrições

- Tamanho máximo de arquivo: 16MB
- Formatos de imagem suportados: JPG, PNG
- Rate limiting: [a ser definido]

## Ambientes

### Produção
- URL Base: a ser definido
- CORS: Domínios específicos permitidos

### Desenvolvimento
- URL Base: `http://localhost:5000`
- CORS: Permite localhost e domínios de desenvolvimento

## Códigos de Erro

- 400: Requisição inválida
- 401: Não autorizado
- 413: Arquivo muito grande
- 415: Formato de arquivo não suportado
- 500: Erro interno do servidor

## Notas de Uso

- Todas as requisições devem incluir cabeçalhos apropriados de Content-Type
- As imagens devem estar em formato claro e de boa qualidade
- Recomenda-se o uso de HTTPS para todas as requisições em produção

## 🚀 Funcionalidades

- **Análise com IA**: Modelo TorchXRayVision para detecção de patologias pulmonares
- **Suporte Multi-formato**: Upload de imagens JPG, PNG e DICOM
- **API RESTful**: Endpoints JSON limpos e organizados
- **CORS Habilitado**: Comunicação frontend-backend
- **Monitoramento de Saúde**: Endpoint integrado de verificação de saúde
- **Suporte em Português**: Nomes de patologias em português

## 🛠️ Stack Tecnológica

- **Framework**: Flask 3.0.3
- **Modelo de IA**: TorchXRayVision
- **Processamento de Imagem**: PIL, NumPy
- **HTTP**: Flask-CORS
- **Implantação**: Pronto para Railway/Heroku

## 🔧 Desenvolvimento

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
python app.py
```

## 🌐 Variáveis de Ambiente

Crie um arquivo `.env`:

```env
FLASK_ENV=production
FLASK_APP=app.py
PYTHONPATH=/app/src
```

## 🐳 Docker

```bash
# Construir imagem
docker build -t lungscan-backend .

# Executar container
docker run -p 5000:5000 lungscan-backend
```

## 📊 Patologias Suportadas

O modelo de IA detecta as seguintes condições pulmonares:

- **Atelectasis** (Atelectasia)
- **Cardiomegaly** (Cardiomegalia)
- **Effusion** (Derrame pleural)
- **Infiltration** (Infiltração)
- **Mass** (Massa)
- **Nodule** (Nódulo)
- **Pneumonia** (Pneumonia)
- **Pneumothorax** (Pneumotórax)
- **Consolidation** (Consolidação)
- **Edema** (Edema)
- **Emphysema** (Enfisema)
- **Fibrosis** (Fibrose)
- **Pleural Thickening** (Espessamento pleural)
- **Hernia** (Hérnia)

## 🔗 Repositório Relacionado

- **Frontend**: [lungscan-frontend](https://github.com/Buscavan/lungscan-frontend)

## 🚀 Implantação

### Railway (Recomendado)

1. Conecte este repositório ao Railway
2. Configure as variáveis de ambiente
3. Implantação automática ao fazer push

### Implantação Manual

```bash
pip install -r requirements.txt
python app.py
```

## ⚠️ Aviso Médico

Este sistema de IA é apenas para fins educacionais. Não deve ser usado como substituto para diagnóstico médico profissional. Sempre consulte profissionais de saúde qualificados para decisões médicas.

## 📝 Licença

Licença MIT - Veja o arquivo [LICENSE](https://github.com/lungscan/lungscan-backend/blob/main/LICENSE) para detalhes 
