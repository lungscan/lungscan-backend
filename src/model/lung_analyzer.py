import torch
import torchvision
import torchxrayvision as xrv
import skimage
import numpy as np
from PIL import Image
import io
from typing import Dict, Union


class LungAnalyzer:
    """
    Lung X-ray analyzer using torchxrayvision for pathology detection.
    """

    def __init__(self, model_name: str = "densenet121-res224-all"):
        """
        Initialize the lung analyzer with a pre-trained model.

        Args:
            model_name (str): Name of the pre-trained model to use
        """
        self.model_name = model_name
        self.model = None
        self.transform = None
        self._load_model()
        self._setup_transforms()

    def _load_model(self):
        """Load the pre-trained torchxrayvision model."""
        try:
            self.model = xrv.models.DenseNet(weights=self.model_name)
            self.model.eval()  # Set to evaluation mode
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load model {self.model_name}: {str(e)}")

    def _setup_transforms(self):
        """Setup image preprocessing transforms."""
        self.transform = torchvision.transforms.Compose([
            xrv.datasets.XRayCenterCrop(),
            xrv.datasets.XRayResizer(224),
        ])

    def preprocess_image(self, image_data: Union[bytes, np.ndarray, str]) -> torch.Tensor:
        """
        Preprocess image data for model inference.

        Args:
            image_data: Image data as bytes, numpy array, or file path

        Returns:
            torch.Tensor: Preprocessed image tensor
        """
        try:
            # Handle different input types
            if isinstance(image_data, bytes):
                # Convert bytes to PIL Image, then to numpy array
                pil_image = Image.open(io.BytesIO(image_data))
                img = np.array(pil_image)
            elif isinstance(image_data, str):
                # Load from file path
                img = skimage.io.imread(image_data)
            elif isinstance(image_data, np.ndarray):
                img = image_data
            else:
                raise ValueError("Unsupported image data type")

            # Normalize to torchxrayvision expected range
            img = xrv.datasets.normalize(img, 255)

            # Convert to single channel if needed
            if len(img.shape) == 3:
                img = img.mean(2)[None, ...]  # Make single color channel
            elif len(img.shape) == 2:
                img = img[None, ...]  # Add channel dimension

            # Apply transforms
            img = self.transform(img)

            # Convert to torch tensor
            img_tensor = torch.from_numpy(img)

            return img_tensor

        except Exception as e:
            raise ValueError(f"Failed to preprocess image: {str(e)}")

    def analyze(self, image_data: Union[bytes, np.ndarray, str]) -> Dict[str, float]:
        """
        Analyze lung X-ray image for pathologies.

        Args:
            image_data: Image data as bytes, numpy array, or file path

        Returns:
            Dict[str, float]: Dictionary mapping pathology names to confidence scores
        """
        try:
            # Preprocess image
            img_tensor = self.preprocess_image(image_data)

            # Run inference
            with torch.no_grad():
                outputs = self.model(img_tensor[None, ...])  # Add batch dimension

            # Convert outputs to dictionary
            results = dict(zip(self.model.pathologies, outputs[0].detach().numpy()))

            # Convert numpy types to Python types for JSON serialization
            results = {k: float(v) for k, v in results.items()}

            return results

        except Exception as e:
            raise RuntimeError(f"Failed to analyze image: {str(e)}")

    def get_pathologies(self) -> list:
        """Get list of pathologies that the model can detect."""
        return self.model.pathologies if self.model else []