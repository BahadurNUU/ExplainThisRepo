import { useLocation } from 'react-router'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Button } from 'react-bootstrap'


export default function DocPage() {
  const location = useLocation();
  const { data: { markdown } } = location.state || {};

  const handleDownload = () => {
    if (!markdown) return;
  
    const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
  
    const link = document.createElement('a');
    link.href = url;
    link.download = 'documentation.md';
    document.body.appendChild(link);
    link.click();
  
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="doc-page" style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      padding: '2rem',
      color: 'white'
    }}>
      <div className="container">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1>Generated Documentation</h1>
          {markdown && (
            <Button 
              variant="outline-light" 
              className="main-btn"
              onClick={handleDownload}
            >
              Download Markdown
            </Button>
          )}
        </div>
        {markdown ? (
          <div className="bg-white p-4 rounded-3 text-black" style={{
            background: 'rgb(40, 42, 54)',
            boxShadow: '0 0 40px rgba(255, 255, 255, 0.5), 0 0 60px rgba(189, 52, 254, 0.2), 0 0 80px rgba(65, 209, 255, 0.1)',
          }}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
          </div>
        ) : (
          <div className="text-center">
            <p>No documentation available. Please generate documentation first.</p>
          </div>
        )}
      </div>
    </div>
  );
}