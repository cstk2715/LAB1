import torch

def test_cuda():
    if torch.cuda.is_available():
        print("CUDA is available!")
        print("Current CUDA version:", torch.version.cuda)
        print("Current CUDA device count:", torch.cuda.device_count())
        print("Current CUDA device name:", torch.cuda.get_device_name(0))
    else:
        print("CUDA is not available!")

test_cuda()
