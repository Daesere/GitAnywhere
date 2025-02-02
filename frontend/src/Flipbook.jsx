import React from "react";
import HTMLFlipBook from "react-pageflip";
import "./Notebook.css";

// Page Component
const Page = React.forwardRef((props, ref) => {
  return (
    <div className="page" ref={ref}>
      <div className="page-content">
        <h2 className="page-header">
          {props.number === 1 && "PERSONAL INFO"}
          {props.number === 2 && "TRIP INFORMATION"}
          {props.number === 3 && "WEATHER"}
          {props.number === 4 && "WRAPPER"}
          {props.number === 5 && "CREDITS"}
          {props.number === 6 && ""}
          </h2>
        <div className="page-text">{props.children}</div>
        <div
          className={
            props.number % 2 === 0 ? "page-footer-right" : "page-footer-left"
          }
       >
          {props.number}
        </div>
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
        <Page number={1}>
          <u>Information </u><br></br>
          &nbsp;&nbsp;&nbsp;&nbsp;First Name: <br></br>
          &nbsp;&nbsp;&nbsp;&nbsp;Weight: <br></br>
          &nbsp;&nbsp;&nbsp;&nbsp;Height: <br></br>
        </Page>
        <Page number={2}>This is the second page. Add more content here!</Page>
        <Page number={3}>You can write anything you want on this page.</Page>
        <Page number={4}>Notebooks are great for organizing thoughts.</Page>
        <Page number={5}>Keep adding pages as needed!</Page>
        <Page number={6}></Page>
      </HTMLFlipBook>

     {/* Navigation Buttons */}
     <div className="controls-left">
        <button onClick={handlePrevPage}>Prev</button>
      </div> 
      <div className="controls-right">
        <button onClick={handleNextPage}>Next</button>
      </div>
    </div>
  );
};

export default Notebook;