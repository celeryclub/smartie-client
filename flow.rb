metadata = {}
reading_header = false
reading_data = false
next_data_bucket = nil

while read file
  if reading_header
    if parse(header)
      reading_header = false
      reading_data = true
      next
    else
      print 'Error: Expected base64 header'
    end
  elsif reading_data && next_data_bucket
    if datum = parse(data)
      metadata[next_data_bucket] = datum.decode
      reading_data = false
      next
    else
      print 'Error: Expected data'
    end
  elsif type, code, length = parse(tag)
    if code == 'mdst'
    elsif code == 'mden'
      print metadata
      metadata = {}
    elsif length > 0
      next_data_bucket = code
      reading_header = true
      next
    elsif length 0
    end
  else
    print 'Error: Expected tag'
  end
end
