
Use of haarcascade_frontalface_default.xml will detect the front face.
Sideview are not able to detect.
Tested images as an input but can't detect if the face is to far, slightly sideview face.

Enhancement Techniques
1. Adjusting brightness and contrast
2. Sharpening images
3. Laplacian Sharpening
4. Median Blur
5. Gaussian Blur
6. Enhanced Coloured

# Flowchart

```mermaid
graph TD
    A([Start]) --> B(1. Camera / 2. Video path /3. Image Enhancer )
    B --> C{x==1}
    B --> D{x==2}
    C --> E[/Detection Process/]
    D --> E
    E --> F[Save the portion of the face detected]
    E --> G[Real Time output using camera]
    G --> F
    B --> I{x==3}
    F --> J[Move to main menu]
    I --> J
    J --> K[Select Image]
    K --> L[/Enhancer techniques/]
    L --> M([Output])
```