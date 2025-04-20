import { useState, useEffect } from 'react'
import { useHttp } from '../hooks/useHttp'
import { toast, ToastContainer } from 'react-toastify'
import { Container, Form, Button, Spinner } from 'react-bootstrap'
import { useNavigate } from 'react-router'

export default function IntroPage() {
  const [repoUrl, setRepoUrl] = useState('')
  const { loading, error, clearError, request } = useHttp()
  const navigate = useNavigate()

  useEffect(() => {
    if (error) {
      toast.error(error);
      console.log('Error caught in useEffect: ', error)
      clearError()
    }
  }, [error])


  const isValidLink = (url) => {
    const regex = /^https:\/\/github\.com\/([A-Za-z0-9_-]+)\/([A-Za-z0-9_-]+)$/
    return regex.test(url)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!repoUrl.trim()) {
      toast.error('Please fill in the repository URL')
      return
    }

    if (isValidLink(repoUrl)) {
      toast.error('Please enter a valid GitHub repository URL')
      return
    }

    try {
      const data = await request('/api/process-repo', 'POST', { repo_url: repoUrl })
      console.log(data)
      if (data) {
        toast.success('Documentation generated successfully')
        setRepoUrl('')
        setTimeout(() => {
          toast.info('Redirecting to documentation...')
          navigate('/doc', { state: { data } })
        }
        , 1000)
      }

    } catch (error) {
      console.log('Catch error while making a request ', error.message)
      toast.error('Error while generating documentation')
    }
    
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <Container style={{ maxWidth: '800px' }}>
        <h1 className="text-center mb-5" style={{ 
          fontSize: '3.5rem', 
          fontWeight: '600',
          background: 'radial-gradient(141.42% 141.42% at 100% 0%,#fff6,#fff0),radial-gradient(140.35% 140.35% at 100% 94.74%,#bd34fe,#bd34fe00),radial-gradient(89.94% 89.94% at 18.42% 15.79%,#41d1ff,#41d1ff00)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          textFillColor: 'transparent'
        }}>
          Generate Docs from GitHub
        </h1>
        <Form onSubmit={handleSubmit} className="bg-white p-4 rounded-3" style={{
          boxShadow: '0 0 40px rgba(255, 255, 255, 0.5), 0 0 60px rgba(189, 52, 254, 0.2), 0 0 80px rgba(65, 209, 255, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.3)'
        }}>
          <Form.Group className="mb-3">
            <Form.Label className="fw-bold">GitHub Repository URL</Form.Label>
            <Form.Control
              type="text"
              placeholder="https://github.com/username/repository"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              required
              className="py-2"
            />
            <Form.Text className="text-muted">
              Paste the URL of the GitHub repository you want to document
            </Form.Text>
          </Form.Group>
          <div className="d-grid">
            <Button 
              variant="primary" 
              type="submit" 
              size="lg"
              className="py-2 main-btn"
            >
              Generate Documentation
              {loading && <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
                style={{marginLeft: '0.5rem'}}
             />}
            </Button>
          </div>
        </Form>
      </Container>
      <ToastContainer />
    </div>
  )
}