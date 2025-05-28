// project_form.js
document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.querySelector('.image-upload input[type="file"]');
  const previewImg = document.getElementById('project-photo-preview');
  const setPhotoLink = document.getElementById('set-project-photo-link');

  // Open file dialog when link is clicked
  setPhotoLink.addEventListener('click', function(e) {
    e.preventDefault();
    fileInput.click();
  });

  // Function to resize image
  function resizeImage(file, maxWidth = 240, maxHeight = 240, quality = 0.8) {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.onload = function() {
        // Calculate new dimensions while maintaining aspect ratio
        let { width, height } = img;
        
        if (width > height) {
          if (width > maxWidth) {
            height = (height * maxWidth) / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width = (width * maxHeight) / height;
            height = maxHeight;
          }
        }
        
        // Set canvas dimensions
        canvas.width = width;
        canvas.height = height;
        
        // Draw and resize image
        ctx.drawImage(img, 0, 0, width, height);
        
        // Convert back to blob
        canvas.toBlob(resolve, 'image/jpeg', quality);
      };
      
      img.src = URL.createObjectURL(file);
    });
  }

  // Show preview when image is selected
  fileInput.addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      try {
        // Resize the image
        const resizedBlob = await resizeImage(file, 300, 300, 0.8);
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(event) {
          previewImg.src = event.target.result;
        };
        reader.readAsDataURL(resizedBlob);
        
        // Optional: Replace the original file with resized version
        const resizedFile = new File([resizedBlob], file.name, {
          type: 'image/jpeg',
          lastModified: Date.now()
        });
        
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(resizedFile);
        fileInput.files = dataTransfer.files;
        
      } catch (error) {
        console.error('Error resizing image:', error);
        // Fallback to original image
        const reader = new FileReader();
        reader.onload = function(event) {
          previewImg.src = event.target.result;
        };
        reader.readAsDataURL(file);
      }
    }
  });
});