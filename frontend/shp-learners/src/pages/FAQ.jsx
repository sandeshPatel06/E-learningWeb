import React, { useState } from 'react';

function FAQ() {
  // Mock FAQ data, combined from static and database examples
  const [faqs, setFaqs] = useState([
    { id: 'db-1', question: 'How do I reset my password?', answer: 'You can reset your password by clicking on the "Forgot Password?" link on the login page.' },
    { id: 'db-2', question: 'What payment methods are accepted?', answer: 'We accept payments via UPI, debit/credit cards, and various digital wallets.' },
    { id: 'db-3', question: 'Can I download course materials?', answer: 'Some courses offer downloadable materials. Check the course details for availability.' },
    { id: 'static-1', question: 'What is this platform about?', answer: 'Our platform provides high-quality online courses across various domains to help you learn and grow your skills.' },
    { id: 'static-2', question: 'How do I buy a course?', answer: 'Choose a course, add it to your cart, and complete the checkout process using UPI, debit/credit cards, or wallets.' },
    { id: 'static-3', question: 'Do you offer certificates?', answer: 'Yes, we provide certificates for most paid courses after successful completion.' },
    { id: 'static-4', question: 'Can I access the course after purchase forever?', answer: 'Yes, once you purchase a course, you get lifetime access unless specified otherwise.' },
    { id: 'static-5', question: 'Is there a mobile app?', answer: 'We are working on our mobile app. Meanwhile, you can access all features through your mobile browser.' },
    { id: 'static-6', question: 'How can I get support?', answer: 'You can email us at <a href="mailto:patelbr5118s@gmail.com" class="text-blue-400 hover:underline">patelbr5118s@gmail.com</a> or use the contact form on our website.' },
  ].filter(faq => faq.answer !== '')); // Filter out empty answers as per Django logic

  const [searchTerm, setSearchTerm] = useState('');
  const [question, setQuestion] = useState('');
  const [showThankYou, setShowThankYou] = useState(false);

  // Filter FAQs based on search term
  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSubmitQuestion = (e) => {
    e.preventDefault();
    if (question.trim()) {
      // Simulate API call to submit question
      console.log('Submitting question:', question);
      // In a real app, you'd send this to your backend
      // On success:
      setQuestion(''); // Clear the textarea
      setShowThankYou(true);
      setTimeout(() => {
        setShowThankYou(false);
      }, 3000); // Hide after 3 seconds
    }
  };

  return (
    <div className="container mx-auto p-4 bg-white rounded-lg shadow-xl border border-gray-200">
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-800">Frequently Asked Questions</h1>

      {/* Search Bar */}
      <div className="search-bar text-center mb-8">
        <input
          type="text"
          id="searchInput"
          placeholder="Search questions..."
          className="w-full md:w-4/5 lg:w-3/4 p-3 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* FAQ List */}
      <div id="faqList">
        {filteredFaqs.length > 0 ? (
          filteredFaqs.map((faq) => (
            <div key={faq.id} className="faq mb-4 border-b border-gray-200 last:border-b-0">
              <input type="checkbox" id={`faq-${faq.id}`} className="hidden" />
              <label htmlFor={`faq-${faq.id}`} className="faq-label flex items-center justify-between p-4 rounded-lg cursor-pointer transition-colors duration-300">
                <span className="text-xl font-semibold text-white">{faq.question}</span>
                <i className="fas fa-chevron-down text-white ml-2"></i> {/* Icon for expand/collapse */}
              </label>
              <div className="faq-content bg-blue-800 text-white p-4 rounded-b-lg transition-all duration-300 ease-in-out max-h-0 overflow-hidden">
                <p dangerouslySetInnerHTML={{ __html: faq.answer }}></p>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-600 py-10">No FAQs match your search.</p>
        )}
      </div>

      {/* Ask Your Own Question */}
      <div className="qa-section text-center mt-12 bg-gray-50 p-6 rounded-lg shadow-inner">
        <h2 className="text-2xl font-bold mb-4 text-blue-800">Have a Question?</h2>
        <form onSubmit={handleSubmitQuestion} className="max-w-xl mx-auto">
          <div className="form-group mb-4">
            <label htmlFor="question" className="sr-only">Your Question</label>
            <textarea
              id="question"
              rows="4"
              placeholder="Type your question here..."
              className="form-control resize-y border border-blue-400 focus:border-blue-600 focus:ring-blue-600"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              required
            ></textarea>
          </div>
          <button type="submit" className="btn bg-blue-900 text-white hover:bg-blue-700 py-3 px-8 text-lg">
            Submit Question
          </button>
        </form>

        {/* Thank You Popup */}
        {showThankYou && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mt-4" role="alert">
            Thank you for your question! We will get back to you shortly.
          </div>
        )}
      </div>

      {/* Feedback Button */}
      <div className="feedback-btn text-center mt-8">
        <a href="mailto:patelbr5118s@gmail.com?subject=Website Feedback" className="btn bg-green-500 text-white hover:bg-green-600 py-3 px-8 text-lg">
          Give Feedback
        </a>
      </div>
    </div>
  );
}

export default FAQ;
