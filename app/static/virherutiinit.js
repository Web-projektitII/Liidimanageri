
document.addEventListener("DOMContentLoaded", function(event) { 
  document.querySelectorAll('.form-control').forEach(
    e => {
      let id = e.id;
      //console.log('addkeyups:'+id);
      e.addEventListener('keyup', e => poistavirhe(id));
      }
    );
  });

    
function poistavirhe(id){
  //console.log(`Täällä:${element_id}`);
  document.querySelectorAll('.has-error').forEach(
    e => {
      if (e.querySelector('#'+id)){   
        e.querySelector('.help-block').remove();
        e.classList.remove('has-error');
        }
      }
    )
}