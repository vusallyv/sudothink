class Sudothink < Formula
  desc "An intelligent terminal assistant that uses OpenAI's GPT-4"
  homepage "https://github.com/vusallyv/sudothink"
  url "https://github.com/vusallyv/sudothink/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"
  head "https://github.com/vusallyv/sudothink.git", branch: "main"

  depends_on "python@3.9"

  def install
    # Install Python package
    system "python3", "-m", "pip", "install", *std_pip_args, "."

    # Install shell scripts
    bin.install "ai.py" => "sudothink"
    share.install "ai.zsh" => "sudothink.zsh"

    # Create completion directory
    (share/"zsh/site-functions").install "sudothink/_ai" if File.exist?("sudothink/_ai")
  end

  def caveats
    <<~EOS
      SudoThink has been installed!

      To get started:

      1. Set your OpenAI API key:
         export OPENAI_API_KEY="your-api-key-here"

      2. Add to your shell configuration:
         echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
         echo 'source #{share}/sudothink.zsh' >> ~/.zshrc

      3. Restart your shell or run:
         source ~/.zshrc

      4. Start using SudoThink:
         ai "find all files larger than 100MB"
         ai "setup a new project" plan
         ai-chat

      For more information, visit: #{homepage}
    EOS
  end

  test do
    system "#{bin}/sudothink", "--help"
  end
end 