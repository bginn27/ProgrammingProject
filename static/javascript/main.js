$(function() {

  var siteSticky = function() {
		$(".js-sticky-header").sticky({topSpacing:0});
	};
	siteSticky();

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();

});

//login page

$(function() {

	$(".input input").focus(function() {
 
	   $(this).parent(".input").each(function() {
		  $("label", this).css({
			 "line-height": "18px",
			 "font-size": "18px",
			 "font-weight": "100",
			 "top": "0px"
		  })
		  $(".spin", this).css({
			 "width": "100%"
		  })
	   });
	}).blur(function() {
	   $(".spin").css({
		  "width": "0px"
	   })
	   if ($(this).val() == "") {
		  $(this).parent(".input").each(function() {
			 $("label", this).css({
				"line-height": "60px",
				"font-size": "24px",
				"font-weight": "300",
				"top": "10px"
			 })
		  });
 
	   }
	});
 
	$(".button").click(function(e) {
	   var pX = e.pageX,
		  pY = e.pageY,
		  oX = parseInt($(this).offset().left),
		  oY = parseInt($(this).offset().top);
 
	   $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
	   $('.x-' + oX + '.y-' + oY + '').animate({
		  "width": "500px",
		  "height": "500px",
		  "top": "-250px",
		  "left": "-250px",
 
	   }, 600);
	   $("button", this).addClass('active');
	})
 
	$(".alt-2").click(function() {
	   if (!$(this).hasClass('material-button')) {
		  $(".shape").css({
			 "width": "100%",
			 "height": "100%",
			 "transform": "rotate(0deg)"
		  })
 
		  setTimeout(function() {
			 $(".overbox").css({
				"overflow": "initial"
			 })
		  }, 600)
 
		  $(this).animate({
			 "width": "140px",
			 "height": "140px"
		  }, 500, function() {
			 $(".box").removeClass("back");
 
			 $(this).removeClass('active')
		  });
 
		  $(".overbox .title").fadeOut(300);
		  $(".overbox .input").fadeOut(300);
		  $(".overbox .button").fadeOut(300);
 
		  $(".alt-2").addClass('material-buton');
	   }
 
	})
 
	$(".material-button").click(function() {
 
	   if ($(this).hasClass('material-button')) {
		  setTimeout(function() {
			 $(".overbox").css({
				"overflow": "hidden"
			 })
			 $(".box").addClass("back");
		  }, 200)
		  $(this).addClass('active').animate({
			 "width": "700px",
			 "height": "700px"
		  });
 
		  setTimeout(function() {
			 $(".shape").css({
				"width": "50%",
				"height": "50%",
				"transform": "rotate(45deg)"
			 })
 
			 $(".overbox .title").fadeIn(300);
			 $(".overbox .input").fadeIn(300);
			 $(".overbox .button").fadeIn(300);
		  }, 700)
 
		  $(this).removeClass('material-button');
 
	   }
 
	   if ($(".alt-2").hasClass('material-buton')) {
		  $(".alt-2").removeClass('material-buton');
		  $(".alt-2").addClass('material-button');
	   }
 
	});
 
 });