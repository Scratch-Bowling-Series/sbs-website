$( document ).ready(function() {




	Scroll('.counter-1 ul', 1);
	Scroll('.counter-2 ul', 1.333);
	Scroll('.counter-3 ul', 1.666);
	Scroll('.counter-4 ul', 2);
	Scroll('.counter-5 ul', 2.333);
	Scroll('.counter-6 ul', 2.666);
	Scroll('.counter-7 ul', 3);

	function Scroll($name, $time)
	{
		$($name).css('transition', 'none');
	    $($name).css('top', '-1335px');
	    $($name).css('transition', 'top ease-out ' + $time + 's'); 
	    setTimeout(function() 
	    {
	    	$($name).css('top', '-65px');
	    	setTimeout(function() 
	    	{   
	    		$($name).css('transition', 'top ease-in .3s');
	    		$($name).css('top', '-75px');
	    	}, 1000 * $time);   
		}, 100);
	}
});