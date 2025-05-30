## SigmaVision

### Overview

**SigmaVision** is a modular image analysis application that integrates classical thresholding techniques with **unsupervised machine learning-based segmentation**. It is designed to process grayscale and color images using both traditional computer vision methods and modern clustering algorithms, enabling side-by-side visualization of results through an interactive GUI.

> This project combines classical image processing with **unsupervised machine learning**, including clustering techniques like **K-means** and **Mean Shift**, to support real-world applications in medical imaging and pattern discovery.

![SegmaVision Overview](https://github.com/user-attachments/assets/b6d5490e-700e-4fbe-94b2-1ecf6a6bbc2c)

---

### Features & Examples

Each feature includes a table with side-by-side **original** and **processed** images for consistent comparison.

---

#### 🔲 Thresholding Techniques

SigmaVision supports a variety of thresholding methods for grayscale images, combining both global and local strategies.
This README showcases global thresholding results only, while local adaptive methods are also implemented in the application.

* **Otsu Thresholding**
* **Optimal Global Thresholding**
* **Spectral Thresholding**

##### Example – Otsu Thresholding

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Otsu Result</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/ff6d72e0-c32c-4900-9337-86a857c856ad" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/b44ca35b-7e0a-49c8-b721-387b9443aa16" width="250"/></td>
</tr>
</table>

> **Insight:** Otsu's method automatically finds an optimal threshold by minimizing intra-class variance. Ideal for bimodal histograms like this one.

---

##### Example – Optimal Thresholding

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Optimal Threshold</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/1fa3767a-6484-4916-a425-21883a2b01ba" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/9933ae13-d39d-4b0d-b02a-1279cc5f8954" width="250"/></td>
</tr>
</table>

> **Insight:** The optimal global threshold balances intensity contrast in a way that highlights object boundaries more prominently.

---

##### Example – Spectral Thresholding

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Spectral Result</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/8b3fc166-4b0e-4d2d-8ac9-736e5359fe42" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/39a30d9c-0f46-4368-96ab-2ccdbe4b6326" width="250"/></td>
</tr>
</table>

> **Insight:** Spectral thresholding applies multi-mode separation, capturing subtle intensity variations beyond simple binary division.

---

#### Unsupervised Machine Learning Segmentation

Includes clustering-based unsupervised ML segmentation for both grayscale and color images:

* **K-Means** – Number of clusters: 3
* **Region Growing** – Tolerance threshold: 20
* **Agglomerative Clustering** – Number of clusters: 8
* **Mean Shift Clustering** – Bandwidth: 10, Spatial radius: 15

---

##### Example – K-Means Clustering

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>K-Means Output</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/77733248-8247-43f2-bd1c-23ea2af882c0" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/975dd435-ca89-4841-a346-f4b5a461e182" width="250"/></td>
</tr>
</table>

> **Insight:** K-means groups similar pixel intensities into 3 distinct clusters, effectively isolating texture zones in the image.

---

##### Example – Region Growing

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Region Grown Output</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/dffda12c-fc92-4025-8613-edd28b152e7e" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/bbb224b2-7883-44f8-b64a-e8ff494f1d43" width="250"/></td>
</tr>
</table>

> **Insight:** Region growing expands from seed points until pixel similarity exceeds the defined threshold. Useful for segmented anatomy or textures.

---

##### Example – Agglomerative Clustering

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Agglomerative Result</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/715d3051-e596-41ac-b49e-8a4f3c1f2b1c" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/88b6e759-424e-4867-86bd-37ea00d8e0b3" width="250"/></td>
</tr>
</table>

> **Insight:** This hierarchical method gradually merges pixel clusters. With 8 clusters, it reveals coarse structure across large visual segments.

---

##### Example – Mean Shift Clustering

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Mean Shift Result</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/60c406db-fa14-4f75-8f9a-b876242df182" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/3c7d5b42-acfc-4f99-929f-a4a85533f5e2" width="250"/></td>
</tr>
</table>

> **Insight:** Mean shift clustering adapts based on local density, revealing object contours and textures without needing to predefine clusters.

---

### Installation

```bash
git clone https://github.com/YassienTawfikk/SegmaVision.git
cd SegmaVision
pip install -r requirements.txt
python main.py
```

---

### Use Cases

* Medical image segmentation (MRI, CT)
* Visual teaching tool for thresholding/clustering
* Research prototyping in unsupervised computer vision
* Comparative evaluation of segmentation algorithms

---

## Contributions

<div>
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/YassienTawfikk" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px;" alt="Yassien Tawfik"/>
        <br />
        <sub><b>Yassien Tawfik</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/nancymahmoud1" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/125357872?v=4" width="150px;" alt="Nancy Mahmoud"/>
        <br />
        <sub><b>Nancy Mahmoud</b></sub>
      </a>
    </td>    
    <td align="center">
      <a href="https://github.com/nariman-ahmed" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/126989278?v=4" width="150px;" alt="Nariman Ahmed"/>
        <br />
        <sub><b>Nariman Ahmed</b></sub>
      </a>
    </td>       
        <td align="center">
      <a href="https://github.com/madonna-mosaad" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/127048836?v=4" width="150px;" alt="Madonna Mosaad"/>
        <br />
        <sub><b>Madonna Mosaad</b></sub>
      </a>
    </td>    
  </tr>
</table>
</div>

---
