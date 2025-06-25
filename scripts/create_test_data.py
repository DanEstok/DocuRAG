"""Create test/mock data for development and testing."""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def create_sample_pdf(filename: str, title: str, content: list, output_dir: str = "data/dev"):
    """Create a sample PDF with given content.
    
    Args:
        filename: Name of the PDF file
        title: Title of the document
        content: List of paragraphs to include
        output_dir: Output directory for the PDF
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        str(output_path / filename),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Build story
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Add content paragraphs
    for i, paragraph in enumerate(content, 1):
        story.append(Paragraph(f"<b>Section {i}</b>", styles['Heading2']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(paragraph, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    print(f"Created: {output_path / filename}")


def create_machine_learning_guide():
    """Create a comprehensive machine learning guide PDF."""
    content = [
        """
        Machine Learning (ML) is a subset of artificial intelligence (AI) that provides systems 
        the ability to automatically learn and improve from experience without being explicitly 
        programmed. Machine learning focuses on the development of computer programs that can 
        access data and use it to learn for themselves.
        """,
        """
        There are three main types of machine learning algorithms: supervised learning, 
        unsupervised learning, and reinforcement learning. Supervised learning uses labeled 
        training data to learn a mapping from inputs to outputs. Common examples include 
        classification and regression problems.
        """,
        """
        Unsupervised learning finds hidden patterns or intrinsic structures in input data 
        without labeled examples. Clustering, association rules, and dimensionality reduction 
        are common unsupervised learning techniques. This approach is useful when you have 
        data but no specific target variable.
        """,
        """
        Reinforcement learning is an area of machine learning concerned with how software 
        agents ought to take actions in an environment to maximize cumulative reward. 
        It differs from supervised learning in that correct input/output pairs need not be 
        presented, and sub-optimal actions need not be explicitly corrected.
        """,
        """
        Deep learning is a subset of machine learning that uses neural networks with multiple 
        layers (deep neural networks) to model and understand complex patterns in data. 
        It has been particularly successful in areas like computer vision, natural language 
        processing, and speech recognition.
        """,
        """
        Common applications of machine learning include recommendation systems, fraud detection, 
        image recognition, natural language processing, autonomous vehicles, and predictive 
        analytics. The field continues to grow rapidly with new techniques and applications 
        being developed regularly.
        """
    ]
    
    create_sample_pdf(
        "machine_learning_guide.pdf",
        "Complete Guide to Machine Learning",
        content
    )


def create_ai_ethics_paper():
    """Create an AI ethics research paper PDF."""
    content = [
        """
        Artificial Intelligence ethics is a branch of ethics specifically concerned with the 
        moral implications of AI systems. As AI becomes more prevalent in society, it's crucial 
        to consider the ethical implications of these technologies and ensure they are developed 
        and deployed responsibly.
        """,
        """
        Key ethical principles in AI include fairness, accountability, transparency, and privacy. 
        Fairness ensures that AI systems do not discriminate against individuals or groups. 
        Accountability means that there should be clear responsibility for AI decisions and 
        their consequences.
        """,
        """
        Transparency in AI refers to the ability to understand how AI systems make decisions. 
        This is particularly important in high-stakes applications like healthcare, criminal 
        justice, and financial services. Explainable AI (XAI) is a growing field focused on 
        making AI decisions more interpretable.
        """,
        """
        Privacy concerns arise when AI systems process personal data. It's essential to protect 
        individual privacy while still enabling beneficial AI applications. Techniques like 
        differential privacy and federated learning help address these concerns.
        """,
        """
        Bias in AI systems can perpetuate or amplify existing societal biases. This can occur 
        through biased training data, algorithmic design choices, or deployment contexts. 
        Addressing bias requires careful attention throughout the AI development lifecycle.
        """,
        """
        The future of AI ethics involves developing robust governance frameworks, establishing 
        industry standards, and fostering collaboration between technologists, ethicists, 
        policymakers, and society at large. Ongoing research and dialogue are essential for 
        responsible AI development.
        """
    ]
    
    create_sample_pdf(
        "ai_ethics_research.pdf",
        "Ethical Considerations in Artificial Intelligence",
        content
    )


def create_data_science_handbook():
    """Create a data science handbook PDF."""
    content = [
        """
        Data Science is an interdisciplinary field that uses scientific methods, processes, 
        algorithms, and systems to extract knowledge and insights from structured and 
        unstructured data. It combines domain expertise, programming skills, and knowledge 
        of mathematics and statistics.
        """,
        """
        The data science process typically follows these steps: problem definition, data 
        collection, data cleaning and preprocessing, exploratory data analysis, feature 
        engineering, model building, model evaluation, and deployment. Each step is crucial 
        for successful data science projects.
        """,
        """
        Python and R are the most popular programming languages for data science. Python 
        offers libraries like pandas, NumPy, scikit-learn, and TensorFlow. R provides 
        excellent statistical computing capabilities with packages like dplyr, ggplot2, 
        and caret.
        """,
        """
        Data visualization is a critical skill for data scientists. Tools like Matplotlib, 
        Seaborn, Plotly, and Tableau help create compelling visualizations that communicate 
        insights effectively. Good visualizations can reveal patterns and trends that might 
        not be apparent in raw data.
        """,
        """
        Statistical analysis forms the foundation of data science. Understanding concepts 
        like hypothesis testing, confidence intervals, correlation, regression, and 
        probability distributions is essential for drawing valid conclusions from data.
        """,
        """
        Big data technologies like Hadoop, Spark, and cloud platforms (AWS, GCP, Azure) 
        enable data scientists to work with large-scale datasets. These tools provide 
        the computational power needed for complex analyses and machine learning at scale.
        """
    ]
    
    create_sample_pdf(
        "data_science_handbook.pdf",
        "The Complete Data Science Handbook",
        content
    )


def create_test_pdfs():
    """Create small test PDFs for unit testing."""
    # Simple test PDF
    simple_content = [
        "This is a simple test document with minimal content for unit testing purposes.",
        "It contains just enough text to test the PDF loading and chunking functionality."
    ]
    
    create_sample_pdf(
        "simple_test.pdf",
        "Simple Test Document",
        simple_content,
        "tests/fixtures"
    )
    
    # Empty-like PDF
    minimal_content = ["Short content."]
    
    create_sample_pdf(
        "minimal_test.pdf",
        "Minimal Test",
        minimal_content,
        "tests/fixtures"
    )


def main():
    """Create all test data."""
    print("Creating development test data...")
    
    try:
        # Create development PDFs
        create_machine_learning_guide()
        create_ai_ethics_paper()
        create_data_science_handbook()
        
        # Create test PDFs
        create_test_pdfs()
        
        print("\n✅ All test data created successfully!")
        print("\nDevelopment PDFs created in: data/dev/")
        print("Test PDFs created in: tests/fixtures/")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install reportlab: pip install reportlab")
    except Exception as e:
        print(f"❌ Error creating test data: {e}")


if __name__ == "__main__":
    main()