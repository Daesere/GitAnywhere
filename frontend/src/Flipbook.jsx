import React from "react";
import HTMLFlipBook from "react-pageflip";
import "./Notebook.css";

// Page Component
const Page = React.forwardRef((props, ref) => {
  return (
    <div className="page" ref={ref}>
      <div className="page-content">
        <h2 className="page-header">Page {props.number}</h2>
        <div className="page-text">{props.children}</div>
        <div className="page-footer">{props.number}</div>
      </div>
    </div>
  );
});

// Notebook Component
const Notebook = () => {
  const flipBookRef = React.useRef(null);

  const handleNextPage = () => {
    if (flipBookRef.current) {
      flipBookRef.current.pageFlip().flipNext();
    }
  };

  const handlePrevPage = () => {
    if (flipBookRef.current) {
      flipBookRef.current.pageFlip().flipPrev();
    }
  };

  return (
    <div className="notebook-container">
      {/* Static Cover */}
      <div className="static-cover"></div>

      {/* Flipbook */}
      <HTMLFlipBook
        width={400} // Fixed width
        height={500} // Fixed height
        size="fixed" // Use "fixed" to prevent resizing
        minWidth={400} // Match the fixed width
        maxWidth={400} // Match the fixed width
        minHeight={500} // Match the fixed height
        maxHeight={500} // Match the fixed height
        maxShadowOpacity={0}
        showCover={false} // Disable covers
        useMouseEvents={false} // Disable mouse events (optional)
        ref={flipBookRef}
        className="notebook"
      >
        {/* Only Pages */}
        <Page number={1}>This is the first page of my notebook.</Page>
        <Page number={2}>This is the second page. Add more content here!</Page>
        <Page number={3}>You can write anything you want on this page.</Page>
        <Page number={4}>Notebooks are great for organizing thoughts.</Page>
        <Page number={5}>Keep adding pages as needed!</Page>
        <Page number={6}>Keep adding pages as needed!</Page>
      </HTMLFlipBook>

     {/* Navigation Buttons */}
     <div className="controls">
        <button onClick={handlePrevPage}>Prev</button>
        <button onClick={handleNextPage}>Next</button>
      </div> 
    </div>
  );
};

export default Notebook;