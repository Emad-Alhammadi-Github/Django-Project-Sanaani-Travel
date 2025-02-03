function openDialog(idDivDialog) {
  const dialog = document.getElementById(idDivDialog);
  dialog.style.display = dialog.style.display === "block" ? "none" : "block";
 
}


 function openEditDialog(vehicleId) {
  let dialogs = document.querySelectorAll('.custom-dialog');
  dialogs.forEach(function(dialog) {
  dialog.style.display = 'none';
  });

  let editDialog = document.getElementById('EditDialog' + vehicleId);
  if (editDialog) {
  editDialog.style.display = 'block';
  }
}

function openDeleteDialog(vehicleId) {
  let dialogs = document.querySelectorAll('.custom-dialog');
  dialogs.forEach(function(dialog) {
  dialog.style.display = 'none';
  });

  let deleteDialog = document.getElementById('DialogDelete' + vehicleId);
  if (deleteDialog) {
  deleteDialog.style.display = 'block';
  }
}

function closeDeleteDialog(vehicleId) {
  let deleteDialog = document.getElementById('DialogDelete' + vehicleId);
  if (deleteDialog) {
  deleteDialog.style.display = 'none';
  }
}

function previewImage(event, imageId) {
  const file = event.target.files[0]; 
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById(imageId).src = e.target.result;
    };
    reader.readAsDataURL(file); 
  }
}


function previewImageee(event, driverId) {
  const file = event.target.files[0];
  const imgElement = document.getElementById(`editImage${driverId}`);
  
  if (file) {
    const reader = new FileReader();
    
    reader.onload = function (e) {
      imgElement.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
  }
}

document.getElementById('upload-button').addEventListener('click', function() {
  document.getElementById('file-input').click(); 
});
// document.getElementById('file-input').addEventListener('change', previewImage);
