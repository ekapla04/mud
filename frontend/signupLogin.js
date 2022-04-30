// Code By Webdevtrick ( https://webdevtrick.com )
/* Edited by Mico */
$('.form').find('input, textarea').on('keyup blur focus', function (e) {
    var $this = $(this),
        label = $this.prev('label');
  
        if (e.type === 'keyup') {
              if ($this.val() === '') {
            label.removeClass('active highlight');
          } else {
            label.addClass('active highlight');
          }
      } else if (e.type === 'blur') {
          if( $this.val() === '' ) {
              label.removeClass('active highlight'); 
              } else {
              label.removeClass('highlight');   
              }   
      } else if (e.type === 'focus') {
        
        if( $this.val() === '' ) {
              label.removeClass('highlight'); 
              } 
        else if( $this.val() !== '' ) {
              label.addClass('highlight');
              }
      }
  });

  $('.form').find('select, textarea').on('keyup blur focus', function (e) {
      var $this = $(this),
          label = $this.prev('label');
    
          if (e.type === 'keyup') {
                if ($this.val() === '') {
              label.removeClass('active highlight');
            } else {
              label.addClass('active highlight');
            }
        } else if (e.type === 'blur') {
            if( $this.val() === '' ) {
                label.removeClass('active highlight'); 
                } else {
                label.removeClass('highlight');   
                }   
        } else if (e.type === 'focus') {
          
          if( $this.val() === '' ) {
                label.removeClass('highlight'); 
                } 
          else if( $this.val() !== '' ) {
                label.addClass('highlight');
                }
        }
    });

  
  $('.tab a').on('click', function (e) {
    console.log("in tab");
    e.preventDefault();
    
    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');
    
    target = $(this).attr('href');
  
    $('.tab-content > div').not(target).hide();
    
    $(target).fadeIn(600);
    
  });

  /* 
    Connect to the server and verify user credentials
    return true if you succeed or false otherwise
  */
  function loginUser(){
    console.log("login user");

    // var loginUsername = localStorage.getItem("logName");
    // var loginPass = localStorage.getItem("logPass");
    // console.log("signup user", loginUsername, loginPass);

    return true;
  }

  /* 
    Connect to the server and sign up user
    return true if you succeed or false otherwise
  */
  function signupUser(){
    // var loginUsername = localStorage.getItem("name");
    // var loginPass = localStorage.getItem("pass");
    console.log("signup user");
    return true;
  }

  