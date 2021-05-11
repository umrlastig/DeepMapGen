
# This work is a model for mountain roads generalisation adapted from cycleGAN that constrain the connectivity measure of input and prediction to be similare.  
This model is presented in the article "Generative Adversarial Networks for Map Generalisation: Better Use Unsupervised Architectures" (not yet published)

# To utilize it and reproduc  the paper results

1. Clone the cycleGAN and Pix2pix PyTorch implementation : git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix
2. Install "cycleGAN and Pix2pix PyTorch implementation" dependencies following the read me information. 
3. Install scikit-image. 
4. Copie thje model file "continuity_constrained_unsupervised_model" in models folder 
5. Separate the image set in four folder train1, trainB, testA and testB, and copie them in a new folder in data section of "cycleGAN and Pix2pix PyTorch implementation"
6. Train the model using: 
python train.py --dataroots .\datasets\datafolder --model connectivity_constrained_unsupervised --name test_name
7. Test and visualize the results. 
python test.py --dataroots .\datasets\datafolder --model connectivity_constrained_unsupervised --name test_name
The test results will be saved to a html file here: `./results/test_name/latest_test/index.html`.


