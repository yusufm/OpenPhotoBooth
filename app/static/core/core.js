$( document ).ready(
	function () {
		$( document ).keypress( function ( e ) { OPBConfig.onKeyPress( e ); } );
		OPBConfig.onLoad();
		$( window ).unload( function () { OPBConfig.onUnload() } );
	}
);

OpenPhotoBooth = {

	capturePending: false,

	captureCallback: function ( imageData ) {
		OpenPhotoBooth.capturePending = false;

		jQuery.ajax(
      {
			 url: "/photo",
			 dataType: 'json',
			 cache: false,
			 async: false,
			 type: "POST",
			 data: { image: imageData },
			 success: function ( data ) { OPBConfig.postCapture( data ); }
		  }
    );

	},

	capture: function () {

		if( OpenPhotoBooth.capturePending )
			return false;

		OPBConfig.preCapture();

		OpenPhotoBooth.capturePending = true;

		// TEST: Cross browser working?
		if( $.browser.msie )
			document.getElementById("swf-object").capture();
		else
			document.getElementById("swf-embed").capture();
	},

	openSet: function () {
		jQuery.ajax(
			{
				url: "/set/open",
				dataType: 'json',
				cache: false,
				async: false,
				data: {}
		  }
		);
	},

	closeSet: function () {
		jQuery.ajax(
			{
				url: "/set/close",
				dataType: 'json',
				cache: false,
				async: false,
				data: {}
		  }
		);
	},

	printSet: function () {
		jQuery.ajax(
			{
				url: "/set/print",
				dataType: 'json',
				cache: false,
				async: false,
				data: {}
		  }
		);
	}
}
