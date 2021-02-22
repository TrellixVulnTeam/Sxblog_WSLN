/*
            /$$
    /$$    /$$$$
   | $$   |_  $$    /$$$$$$$
 /$$$$$$$$  | $$   /$$_____/
|__  $$__/  | $$  |  $$$$$$
   | $$     | $$   \____  $$
   |__/    /$$$$$$ /$$$$$$$/
          |______/|_______/
================================
        Keep calm and get rich.
                    Is the best.

  	@Author: Dami
  	@Date:   2017-09-06 15:27:44
 * @Last Modified by: Vv
 * @Last Modified time: 2019-08-18 01:00:17
*/
window.$ = jQuery;
var isApollo = $("meta[name=apollo-enabled]").attr("content") === '1';

// mobile Sidebar
function toggleSidebar() {
    $('.sidebar-close, .mobile-overlay').on('click', function () {
        $('body').removeClass('modal-open');
        $('.mobile-sidebar').removeClass('active');
        $('.mobile-overlay').removeClass('active');
    });
    $('#sidebarCollapse').on('click', function () {
        $('body').addClass('modal-open');
        $('.mobile-sidebar').addClass('active');
        $('.mobile-overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
}
jQuery(document).ready(function($)  {
    toggleSidebar();

    $(window).scroll(function() {
        var $window = $(window),
            $window_width = $window.width();

        if ($(this).scrollTop() > 200 && $window_width >= 1024) {
            $('#scroll_to_top').filter(':hidden').fadeIn('fast');
        } else {
            $('#scroll_to_top').filter(':visible').fadeOut('fast');
        }
    });
    $('#scroll_to_top').on('click',
    function() {
        $('html, body').animate({
            scrollTop: 0
        },
        'slow');
        return false;
    });

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                scrollTop: (target.offset().top - 60)
                }, 1000, "easeInOutExpo");
            return false;
            }
        }
    });

    // Tooltip
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').on('shown.bs.tooltip', function () {
        $('.tooltip').addClass('animated fadeIn');
    })

    // theiaStickySidebar
    $('.sidebar').theiaStickySidebar({
        additionalMarginTop: 20,
        additionalMarginBottom: 20
    });
    // theiaStickySidebar
    $('.sidebar-author').theiaStickySidebar({
        additionalMarginTop: 100,
        additionalMarginBottom: 20
    });
    if ($(".main-menu li").hasClass("menu-item-has-children")) {
        $('.main-menu .menu-item-has-children').prepend('<span class="icon-sub-menu"><i class="iconfont icon-arrow-down-s-line"></i></span>')
    };
    $('.mobile-sidebar-menu .menu-item-has-children > a').append('<div class="dropdown-sub-menu"><span class="iconfont icon-arrow-drop-down-fill"></span></div>'),
    $('.dropdown-sub-menu').on("click",
    function() {
        $(this).parents('li').children('.sub-menu').slideToggle(),
        $(this).parents('li').children('.dropdown-sub-menu').toggleClass('current')
    });


    // carousel
    var owl = $('.list-banner .owl-carousel');
    if (owl.length > 0) {
        owl.owlCarousel({
            items:1,
            loop:true,
            margin:10,
            smartSpeed:1000,
            autoplay:true,
            autoplayTimeout:5000,
            autoplayHoverPause:true,
            responsiveClass:true,
			responsive:{
				0:{
					items:1,
                    margin:10,
                    nav: false,
				},
				768:{
					nav: true,
                    navText:['<i class="iconfont icon-left"></i>','<i class="iconfont icon-right"></i>'],
				},
				992:{
					nav: true,
                    navText:['<i class="iconfont icon-left"></i>','<i class="iconfont icon-right"></i>'],
				}
			}
        });
    }

   

   


   

    $(document).on('click', '.single-popup', function(event) {
        event.preventDefault();
        var img = $(this).data("img");
        var title = $(this).data("title");
        var desc = $(this).data("desc");
        var html = '<div class="text-center"><h6 class="py-1">' + title + '</h6>\
                    <div class="text-muted text-sm mb-2" > '+ desc +' </div>\
                    <img src="' + img + '" alt="' + title + '" style="width:100%;height:auto;">\
                    </div>'
        ncPopup('small', html)
    });
    $(document).on('click', '.plus-power-popup', function (event) {
        event.preventDefault();
        var $this = $('#plus-power-popup-wrap');
        ncPopup('no-padding', $this.html())
    });
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document. documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document. documentElement.clientWidth)
        );
    }
    function givenElementInViewport (el, fn) {
        return function () {
            if (isElementInViewport(el)) {
                fn.call();
            }
        }
    }
    function addViewportEvent (el, fn) {
        if (window.addEventListener) {
            addEventListener('DOMContentLoaded', givenElementInViewport(el, fn), false);
            addEventListener('load', givenElementInViewport(el, fn), false);
            addEventListener('scroll', givenElementInViewport(el, fn), false);
            addEventListener('resize', givenElementInViewport(el, fn), false);
        } else if (window.attachEvent)  {
            attachEvent('DOMContentLoaded', givenElementInViewport(el, fn));
            attachEvent('load', givenElementInViewport(el, fn));
            attachEvent('scroll', givenElementInViewport(el, fn));
            attachEvent('resize', givenElementInViewport(el, fn));
        }
    }


   

   

    $(document).on('click', '.link-post-share', function (event) {
        event.preventDefault();
        $(this).parent().toggleClass('show');
        $('body').toggleClass('modal-open');
        $('.mobile-overlay').addClass('active');
    });
    if ($('.content-share').hasClass('show') === false) {
        $(document).on('click', '.nice-dropdown .weixin, .mobile-overlay', function (event) {
            event.preventDefault();
            $('.content-share').removeClass('show');
            $('body').removeClass('modal-open');
            $('.mobile-overlay').removeClass('active');
        });
    }
   



});// End of use strict

